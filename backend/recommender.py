"""
Simple content-based recommendation engine for the Collect project.

This module computes cosine similarity between a user preference vector
or a seed track and all other tracks to produce top-N recommendations.
"""

from __future__ import annotations

from math import sqrt
from typing import Dict, Iterable, List, Tuple

from .data import TRACKS, extract_feature_vector, get_track_index_by_id


FeatureVector = Dict[str, float]


def _dot(a: FeatureVector, b: FeatureVector) -> float:
    return sum(a[k] * b[k] for k in a.keys())


def _norm(a: FeatureVector) -> float:
    return sqrt(sum(v * v for v in a.values()))


def cosine_similarity(a: FeatureVector, b: FeatureVector) -> float:
    denom = _norm(a) * _norm(b)
    if denom == 0:
        return 0.0
    return _dot(a, b) / denom


def build_preference_vector(
    *,
    danceability: float | None = None,
    energy: float | None = None,
    valence: float | None = None,
    tempo: float | None = None,
) -> FeatureVector:
    # Fill missing values with midpoints for neutral bias
    return {
        "danceability": float(danceability if danceability is not None else 0.5),
        "energy": float(energy if energy is not None else 0.5),
        "valence": float(valence if valence is not None else 0.5),
        "tempo": float(tempo if tempo is not None else 0.5),
    }


def recommend_by_seed_track(seed_track_id: str, k: int = 5) -> List[Dict]:
    idx = get_track_index_by_id(seed_track_id)
    if idx < 0:
        return []
    seed = TRACKS[idx]
    seed_vec = extract_feature_vector(seed)
    scored: List[Tuple[float, Dict]] = []
    for t in TRACKS:
        if t["id"] == seed_track_id:
            continue
        v = extract_feature_vector(t)
        s = cosine_similarity(seed_vec, v)
        scored.append((s, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored[:k]]


def recommend_by_preferences(prefs: FeatureVector, k: int = 5) -> List[Dict]:
    scored: List[Tuple[float, Dict]] = []
    for t in TRACKS:
        v = extract_feature_vector(t)
        s = cosine_similarity(prefs, v)
        scored.append((s, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored[:k]]


