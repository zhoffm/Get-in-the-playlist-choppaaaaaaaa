# TODO: 

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import arrow

logging.basicConfig(level='WARNING')

username = 'zhoffm'
user_id = 121776799
scope = "user-library-read,playlist-modify-private,playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))


def create_playlist(playlist_name, description=''):
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=description)
    if new_playlist.get('id'):
        return new_playlist.get('id')
    return new_playlist


def add_songs_to_playlist(playlist_id, tracklist):
    track_id_list = strip_ids_from_tracklist(tracklist)
    sp.user_playlist_add_tracks(playlist_id, track_id_list)


def get_100_tracks(offset=0):
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    tracks = results.get("items")

    while len(tracks) % 100 != 0:
        results = sp.next(results)
        logging.info(results.get("items"))
        tracks.extend(results.get("items"))

    return results.get('next'), tracks


def strip_ids_from_tracklist(results):
    results_ids = [result.get('track').get('id') for result in results if results.get('track')]
    return results_ids


def get_all_tracks():
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results.get("items")

    while results.get("next"):
        results = sp.next(results)
        logging.info(results.get("items"))
        tracks.extend(results.get("items"))

    return tracks


if __name__ == '__main__':
    # created_playlist = create_playlist('test_playlist')
    # print(created_playlist)
    offset = 0
    next_batch, tracklist = get_100_tracks()


