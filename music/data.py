"""All of the app's content lives here instead of in a database.

To change the songs, edit RAW_SONGS. To make a song play real audio, drop a file named
after its slug into music/static/music/audio/ (see README.md for the exact names).
"""
from pathlib import Path

from django.utils.text import slugify

STATIC_DIR = Path(__file__).resolve().parent / "static" / "music"

# (title, artist, length in seconds, play count used to rank "Trending now")
RAW_SONGS = [
    ("Kabisado", "IV of Spades", 203, 640),
    ("Sino", "Unique Salonga", 187, 520),
    ("Circles", "Post Malone", 224, 910),
    ("Blinding Lights", "The Weeknd", 198, 980),
    ("I knew it, i knew you", "Taylor Swift", 241, 870),
    ("Magbalik", "Callalily", 176, 430),
    ("Chasing cars", "Snow", 215, 700),
    ("Saksi and langit", "December Avenue", 192, 480),
    ("Fireworks", "Katy perry", 208, 760),
    ("Juno", "Sabrina Carpenter", 233, 820),
    ("Money Trees", "Kendrick Lamar & Jay Rock", 169, 560),
    ("NOKIA", "Drake", 251, 610),
]

AUDIO_EXTENSIONS = (".mp3", ".m4a", ".ogg", ".wav")
COVER_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def _find(folder, slug, extensions):
    """Return the static path of a matching file, or "" if it isn't there."""
    for extension in extensions:
        if (STATIC_DIR / folder / f"{slug}{extension}").exists():
            return f"music/{folder}/{slug}{extension}"
    return ""


def all_songs():
    # Built on every request so newly added audio files are picked up without a restart.
    songs = []
    for number, (title, artist, duration, plays) in enumerate(RAW_SONGS, start=1):
        slug = slugify(title)
        minutes, seconds = divmod(duration, 60)
        songs.append(
            {
                "id": number,
                "title": title,
                "artist": artist,
                "slug": slug,
                "duration": duration,
                "duration_display": f"{minutes}:{seconds:02d}",
                "plays": plays,
                "audio": _find("audio", slug, AUDIO_EXTENSIONS),
                "cover": _find("covers", slug, COVER_EXTENSIONS),
            }
        )
    return songs


def get_song(pk):
    return next((song for song in all_songs() if song["id"] == pk), None)


def _playlist_song_ids(number):
    start = ((number - 1) * 2) % len(RAW_SONGS)
    return [((start + offset) % len(RAW_SONGS)) + 1 for offset in range(4)]


PLAYLISTS = [
    {"id": number, "name": f"Playlist #{number}", "song_ids": _playlist_song_ids(number)}
    for number in range(1, 10)
]
