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


def main() -> None:
    """Load the catalog and print recommendations for the default profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    print_recommendations("Happy Pop (default)", user_prefs, songs)


if __name__ == "__main__":
    main()
