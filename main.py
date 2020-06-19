import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

logging.basicConfig(level=logging.DEBUG)

username = 'zhoffm'
scope = "user-library-read,playlist-modify-private,playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))


def make_playlist():
    pass

def get_100_songs():
    pass


results = sp.current_user_saved_tracks()
tracks = results.get("items")

while results.get("next"):
    results = sp.next(results)
    logging.info(results.get("items"))
    tracks.extend(results.get("items"))

print(len(tracks))
