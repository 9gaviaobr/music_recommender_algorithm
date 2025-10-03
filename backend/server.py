"""
Minimal Python HTTP server (standard library only) for the Collect project.

Features:
- Serves static frontend from ../frontend
- Exposes a tiny AI-like recommendations API at /api/recommend

Run:
  py backend/server.py
Then open http://127.0.0.1:8000
"""

from __future__ import annotations

import json
import os
import posixpath
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict

from .data import get_tracks
from .recommender import (
    build_preference_vector,
    recommend_by_preferences,
    recommend_by_seed_track,
)


ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"


def _parse_float(qs: Dict[str, str], key: str) -> float | None:
    val = qs.get(key)
    if val is None:
        return None
    try:
        return float(val)
    except ValueError:
        return None


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        # Serve files from the frontend directory by default
        # Copied/modified from SimpleHTTPRequestHandler implementation
        path = path.split("?", 1)[0]
        path = path.split("#", 1)[0]
        trailing_slash = path.rstrip().endswith("/")
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split("/")
        words = [_f for _f in words if _f]
        fullpath = FRONTEND_DIR
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            fullpath = fullpath / word
        if trailing_slash:
            return str(fullpath / "index.html")
        return str(fullpath)

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.handle_api()
        return super().do_GET()

    def handle_api(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/tracks":
            return self._json({"tracks": get_tracks()})
        if parsed.path == "/api/recommend":
            qs = dict(urllib.parse.parse_qsl(parsed.query))
            seed = qs.get("seed")
            k = int(qs.get("k", "5"))
            if seed:
                recs = recommend_by_seed_track(seed, k=k)
                return self._json({"recommendations": recs})
            # From preferences
            prefs = build_preference_vector(
                danceability=_parse_float(qs, "danceability"),
                energy=_parse_float(qs, "energy"),
                valence=_parse_float(qs, "valence"),
                tempo=_parse_float(qs, "tempo"),
            )
            recs = recommend_by_preferences(prefs, k=k)
            return self._json({"recommendations": recs})
        self.send_error(404, "Not Found")

    def log_message(self, format: str, *args):  # quieter logs
        return

    def _json(self, payload: Dict):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    addr = ("127.0.0.1", 8000)
    httpd = HTTPServer(addr, Handler)
    print(f"Serving on http://{addr[0]}:{addr[1]}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()


