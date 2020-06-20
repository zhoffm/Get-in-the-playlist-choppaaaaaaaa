# TODO: 

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

logging.basicConfig(level=logging.DEBUG)

username = 'zhoffm'
user_id = 121776799
scope = "user-library-read,playlist-modify-private,playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))


def make_playlist():
    # sp.user_playlist_create(username, )
    pass

def add_songs_to_playlist():
    pass

def get_100_songs():
    pass


results = sp.current_user_saved_tracks(limit=50)
tracks = results.get("items")
print(tracks)
print(sp.next(results))

# while results.get("next"):
#     results = sp.next(results)
#     logging.info(results.get("items"))
#     tracks.extend(results.get("items"))

print(len(tracks))
