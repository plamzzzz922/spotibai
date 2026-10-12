from .data import all_songs


def songs_json(request):
    """Gives every template the song list used by the now-playing bar."""
    return {
        "songs_json": [
            {"id": s["id"], "title": s["title"], "artist": s["artist"]} for s in all_songs()
        ]
    }
