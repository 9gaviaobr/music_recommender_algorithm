"""
Sample music dataset for the Collect project.

Each track includes simple content features to demonstrate how an AI
recommendation system might work. This is intentionally small and
readable for educational purposes.
"""

from typing import Dict, List, TypedDict


class Track(TypedDict):
    id: str
    title: str
    artist: str
    genre: str
    year: int
    # Simple content features scaled roughly 0..1 for demo
    danceability: float
    energy: float
    valence: float  # musical positivity
    tempo_bpm: int


# Tiny curated dataset across genres and moods
TRACKS: List[Track] = [
    {
        "id": "t001",
        "title": "Neon Skyline",
        "artist": "Violet Streets",
        "genre": "synthpop",
        "year": 2021,
        "danceability": 0.78,
        "energy": 0.72,
        "valence": 0.65,
        "tempo_bpm": 118,
    },
    {
        "id": "t002",
        "title": "Lofty",
        "artist": "Chill District",
        "genre": "lofi",
        "year": 2020,
        "danceability": 0.62,
        "energy": 0.35,
        "valence": 0.54,
        "tempo_bpm": 82,
    },
    {
        "id": "t003",
        "title": "Thunder Run",
        "artist": "Analog Kings",
        "genre": "rock",
        "year": 2018,
        "danceability": 0.55,
        "energy": 0.86,
        "valence": 0.48,
        "tempo_bpm": 142,
    },
    {
        "id": "t004",
        "title": "Sun Daze",
        "artist": "Ocean Avenue",
        "genre": "indie",
        "year": 2019,
        "danceability": 0.70,
        "energy": 0.58,
        "valence": 0.80,
        "tempo_bpm": 104,
    },
    {
        "id": "t005",
        "title": "Night Shift",
        "artist": "Deep Circuit",
        "genre": "house",
        "year": 2022,
        "danceability": 0.90,
        "energy": 0.77,
        "valence": 0.62,
        "tempo_bpm": 124,
    },
    {
        "id": "t006",
        "title": "Echoes",
        "artist": "Wide Fields",
        "genre": "ambient",
        "year": 2017,
        "danceability": 0.18,
        "energy": 0.20,
        "valence": 0.40,
        "tempo_bpm": 60,
    },
    {
        "id": "t007",
        "title": "City Lights",
        "artist": "Mono Metro",
        "genre": "hiphop",
        "year": 2023,
        "danceability": 0.82,
        "energy": 0.69,
        "valence": 0.56,
        "tempo_bpm": 96,
    },
    {
        "id": "t008",
        "title": "Golden Hour",
        "artist": "Folkways",
        "genre": "folk",
        "year": 2016,
        "danceability": 0.48,
        "energy": 0.37,
        "valence": 0.74,
        "tempo_bpm": 88,
    },
]


def get_tracks() -> List[Track]:
    return TRACKS


def get_track_index_by_id(track_id: str) -> int:
    for i, t in enumerate(TRACKS):
        if t["id"] == track_id:
            return i
    return -1


def extract_feature_vector(track: Track) -> Dict[str, float]:
    """
    Extracts a normalized numeric feature vector from a track. Tempo is scaled
    down to 0..1 using a simple min/max common range for demo purposes.
    """
    tempo_scaled = (track["tempo_bpm"] - 60) / (160 - 60)  # assume 60..160 BPM
    return {
        "danceability": float(track["danceability"]),
        "energy": float(track["energy"]),
        "valence": float(track["valence"]),
        "tempo": float(max(0.0, min(1.0, tempo_scaled))),
    }



