# TODO: ALLLLLLL OF IT

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import arrow
import operator

logging.basicConfig(level='DEBUG')

username = 'zhoffm'
user_id = 121776799
scope = "user-library-read,playlist-modify-private,playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))


def chop_liked_songs():
    offset = get_total_number_liked_songs() - 50
    logging.info(f'Current Position: {offset}')
    more_tracks, track_batch = get_100_tracks(offset)

    while more_tracks:
        playlist_name = create_playlist_name(track_batch)
        new_playlist = create_playlist(playlist_name)
        add_songs_to_playlist(new_playlist.get('id'), track_batch)
        offset -= 100
        if offset < 0:
            return
        logging.info(f'Current Position: {offset}')
        more_tracks, track_batch = get_100_tracks(offset)


def get_all_playlists():
    results = sp.user_playlists(user_id, limit=50)
    logging.debug(results)
    playlists = results.get("items")

    while results.get("next"):
        results = sp.next(results)
        logging.debug(results.get("items"))
        playlists.extend(results.get("items"))

    return playlists


def create_playlist_name(track_list):
    logging.info(f'Track List: {track_list}')
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
    logging.debug(track_id_list)
    sp.user_playlist_add_tracks(user_id, playlist_id, track_id_list)


# TODO: Change this function because offset!=pagination
def get_100_tracks(offset):
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    logging.debug(results)
    tracks = results.get('items')

    if results.get('previous'):
        results = sp.previous(results)
    if results:
        logging.info(results.get('items'))
        tracks = results.get('items') + tracks

    return results.get('previous'), tracks


def verify_order_by_time_added(track_list):
    unsorted_track_list = track_list
    logging.debug(unsorted_track_list)
    track_list.sort(key=operator.itemgetter('added_at'), reverse=True)
    logging.debug(track_list)
    return unsorted_track_list == track_list


def strip_ids_from_tracklist(results):
    results_ids = [result.get('track').get('id') for result in results if result.get('track')]
    return results_ids


def get_total_number_liked_songs():
    results = sp.current_user_saved_tracks()
    return results.get('total')


def get_all_tracks():
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results.get("items")

    while results.get("next"):
        results = sp.next(results)
        logging.info(results.get("items"))
        tracks.extend(results.get("items"))

    return tracks


if __name__ == '__main__':
    # offset = get_total_number_liked_songs() - 50
    # more_tracks, track_batch = get_100_tracks(offset)
    # playlist_name = create_playlist_name(track_batch)
    # new_playlist = create_playlist(playlist_name)
    # add_songs_to_playlist(new_playlist.get('id'), track_batch)
    chop_liked_songs()

