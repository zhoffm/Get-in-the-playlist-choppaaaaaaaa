# TODO: ALLLLLLL OF IT

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import arrow

logging.basicConfig(level='DEBUG')

username = 'zhoffm'
user_id = 121776799
scope = "user-library-read,playlist-modify-private,playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))


def chop_liked_songs():
    offset = 0
    more_tracks, track_batch = get_100_tracks(offset)
    while more_tracks:
        track_id_list = strip_ids_from_tracklist(track_batch)
        # new_playlist = create_playlist(playlist_name, )
        offset += 1


def get_all_playlists():
    results = sp.user_playlists(user_id, limit=50)
    logging.debug(results)
    playlists = results.get("items")

    while results.get("next"):
        results = sp.next(results)
        logging.info(results.get("items"))
        playlists.extend(results.get("items"))

    return playlists


def create_playlist_name(track_list):
    logging.info(track_list)
    if track_list:
        start_track_name = track_list[0].get('track').get('name')
        end_track_name = track_list[-1].get('track').get('name')
        new_playlist_name = f'{start_track_name} - {end_track_name}'
        logging.info(f'New playlist name: {new_playlist_name}')
        return new_playlist_name


def create_playlist(playlist_name, description=''):
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=description)
    logging.debug(new_playlist)
    return new_playlist


def add_songs_to_playlist(playlist_id, tracklist):
    track_id_list = strip_ids_from_tracklist(tracklist)
    sp.user_playlist_add_tracks(user_id, playlist_id, track_id_list)


# TODO: Change this function because offset!=pagination
def get_100_tracks(offset=0):
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    tracks = results.get('items')

    while len(tracks) % 100 != 0:
        results = sp.next(results)
        logging.info(results.get('items'))
        tracks.extend(results.get('items'))

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
    next_batch, tracklist = get_100_tracks(offset=1)
    print(next_batch, tracklist)
    create_playlist_name(tracklist)


