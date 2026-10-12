# Spotibai (web view, no database)

A desktop web music app built with Django templates, adapted from a mobile Figma wireframe.
The wide layout has a sidebar, a top search bar and a now-playing bar; on a narrow window the sidebar becomes a top strip.
There is **no database, no admin and no login system**. Songs are listed in `music/data.py`,
and every page is reached by clicking icons and links.

## Pages

| Wireframe | Page | URL |
|---|---|---|
| Frame 3 | Login (and Create account) | `/login/`, `/register/` |
| Frame 2 | Home (liked songs, playlists, trending, mini player) | `/` |
| Frame 4 | Music player | `/play/<id>/` |
| Frame 6 | Account (Recent Music, Settings, Log Out) | `/account/` |
| Frame 7 | Liked songs | `/liked/` |
| Frame 5 | My Playlist | `/playlists/` |

Extra pages: search, trending, playlist detail, recent music, settings.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/ . There is nothing to migrate or seed.

## How it works without a database

- `music/data.py` holds the songs and playlists as plain Python lists.
- Liked songs and recent music are saved in the browser (`localStorage`) by `music/static/music/app.js`.
  Settings has a button that resets them.
- Login and Create account are look-alike screens: the button just opens Home.

## Playing real songs

Put an audio file in `music/static/music/audio/` named after the song, then refresh.
Songs with no file still open the player and run a pretend progress bar.

| Song | Artist | File name |
|---|---|---|
| Kabisado | IV of Spades | `kabisado.mp3` |
| Sino | Unique Salonga | `sino.mp3` |
| Circles | Post Malone | `circles.mp3` |
| Blinding Lights | The Weeknd | `blinding-lights.mp3` |
| I knew it, i knew you | Taylor Swift | `i-knew-it-i-knew-you.mp3` |
| Magbalik | Callalily | `magbalik.mp3` |
| Chasing cars | Snow | `chasing-cars.mp3` |
| Saksi and langit | December Avenue | `saksi-and-langit.mp3` |
| Fireworks | Katy perry | `fireworks.mp3` |
| Juno | Sabrina Carpenter | `juno.mp3` |
| Money Trees | Kendrick Lamar & Jay Rock | `money-trees.mp3` |
| NOKIA | Drake | `nokia.mp3` |

Cover images work the same way: `music/static/music/covers/<name>.jpg` (or `.png`, `.webp`).
Audio files are ignored by Git so they are not pushed to GitHub.

## Project layout

- `config/` settings and root URLs
- `music/data.py` songs and playlists
- `music/views.py` one view per page
- `music/templates/music/` `base.html` plus one template per page
- `music/static/music/` `style.css`, `app.js` (likes, recent, mini player), `player.js` (play/pause)
