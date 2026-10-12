from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .data import PLAYLISTS, all_songs, get_song


def _trending(songs):
    return sorted(songs, key=lambda song: -song["plays"])


def login_page(request):
    return render(request, "music/login.html")


def register_page(request):
    return render(request, "music/register.html")


def home(request):
    songs = all_songs()
    return render(
        request,
        "music/home.html",
        {
            "songs": songs,  # every song is rendered; the browser shows only the liked ones
            "trending": _trending(songs)[:6],
            "playlists": PLAYLISTS[:6],
        },
    )


def search(request):
    query = request.GET.get("q", "").strip().lower()
    songs = all_songs()
    if query:
        results = [s for s in songs if query in s["title"].lower() or query in s["artist"].lower()]
        title = "Search results"
        empty = "No songs match that search. Try a title or an artist."
    else:
        results = []
        title = "Search"
        empty = "Type a song title or an artist on the home page to search."
    return render(
        request,
        "music/song_grid.html",
        {"title": title, "songs": results, "empty_message": empty},
    )


def trending(request):
    return render(
        request,
        "music/song_grid.html",
        {
            "title": "Trending now",
            "songs": _trending(all_songs()),
            "empty_message": "No songs yet.",
        },
    )


def liked_songs(request):
    return render(
        request,
        "music/song_grid.html",
        {
            "title": "Liked Songs",
            "songs": all_songs(),
            "collection": "liked",
            "empty_message": "Tap the star on a song to save it here.",
        },
    )


def playlists(request):
    return render(request, "music/playlists.html", {"playlists": PLAYLISTS})


def playlist_detail(request, pk):
    playlist = next((p for p in PLAYLISTS if p["id"] == pk), None)
    if playlist is None:
        raise Http404("No such playlist")
    by_id = {song["id"]: song for song in all_songs()}
    return render(
        request,
        "music/song_grid.html",
        {
            "title": playlist["name"],
            "songs": [by_id[i] for i in playlist["song_ids"] if i in by_id],
            "empty_message": "This playlist is empty.",
            "back_url": reverse("playlists"),
        },
    )


def player(request, pk):
    songs = all_songs()
    position = next((i for i, song in enumerate(songs) if song["id"] == pk), None)
    if position is None:
        raise Http404("No such song")
    return render(
        request,
        "music/player.html",
        {
            "song": songs[position],
            "prev_song": songs[position - 1],  # index -1 wraps to the last song
            "next_song": songs[(position + 1) % len(songs)],
        },
    )


def account(request):
    return render(request, "music/account.html")


def recent(request):
    return render(
        request,
        "music/song_grid.html",
        {
            "title": "Recent Music",
            "songs": all_songs(),
            "collection": "recent",
            "empty_message": "Songs you play will show up here.",
            "back_url": reverse("account"),
        },
    )


def settings_page(request):
    return render(request, "music/settings.html")
