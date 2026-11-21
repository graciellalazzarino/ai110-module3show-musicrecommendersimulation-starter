import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

# Algorithm Recipe weights (see README "Planned scoring rule")
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 1.0
ACOUSTIC_POINTS = 0.5

NUMERIC_FIELDS = {
    "id": int,
    "energy": float,
    "tempo_bpm": float,
    "valence": float,
    "danceability": float,
    "acousticness": float,
}


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, best first."""
        prefs = asdict(user)
        return sorted(
            self.songs,
            key=lambda song: score_song(prefs, asdict(song))[0],
            reverse=True,
        )[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of how a song was scored for this user."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field, convert in NUMERIC_FIELDS.items():
                row[field] = convert(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and list the reasons."""
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    # Closeness, not "higher is better": 1.0 for a perfect match, less as the gap grows.
    target = user_prefs["target_energy"]
    energy_score = ENERGY_POINTS * (1 - abs(song["energy"] - target))
    score += energy_score
    reasons.append(f"energy {song['energy']:.2f} vs target {target:.2f} (+{energy_score:.2f})")

    acoustic = song["acousticness"]
    if user_prefs["likes_acoustic"]:
        acoustic_score = ACOUSTIC_POINTS * acoustic
        label = "acoustic"
    else:
        acoustic_score = ACOUSTIC_POINTS * (1 - acoustic)
        label = "produced"
    score += acoustic_score
    reasons.append(f"{label} sound, acousticness {acoustic:.2f} (+{acoustic_score:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort from highest to lowest, and return the top k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
