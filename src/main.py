"""
Command line runner for the Music Recommender Simulation.

Run from the project folder with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a readable, ranked list of recommendations for one profile."""
    print("=" * 64)
    print(f"Profile: {profile_name}")
    print(
        f"  genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 64)

    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}, {song['mood']}]")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
        print()


PROFILES = {
    # Main profiles
    "Happy Pop (default)": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    # Edge cases: profiles meant to trick or stress the scoring logic
    "EDGE: Sad but High Energy": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": True,
    },
    "EDGE: Genre Not In Catalog": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.7,
        "likes_acoustic": False,
    },
    "EDGE: Acoustic Metalhead": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
}


def main() -> None:
    """Load the catalog and print recommendations for every test profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
