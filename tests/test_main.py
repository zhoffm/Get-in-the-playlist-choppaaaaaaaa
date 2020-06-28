import pytest
import spotipy
import logging
from spotipy.oauth2 import SpotifyOAuth
from main import create_playlist, \
    get_all_playlists, \
    get_all_tracks, \
    verify_order_by_time_added, \
    get_100_tracks, \
    get_total_number_liked_songs

logging.basicConfig(level='DEBUG')


class TestPlaylistChopper:
    username = 'zhoffm'
    user_id = 121776799
    scope = "user-library-read,playlist-modify-private,playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))

    @pytest.fixture()
    def create_test_playlist(self):
        test_playlist_name = 'TEST_PLAYLIST_01'
        test_playlist_description = 'TEST PLAYLIST DESCRIPTION'
        new_test_playlist = create_playlist(test_playlist_name, test_playlist_description)
        logging.info(new_test_playlist)
        yield new_test_playlist

    @pytest.fixture()
    def get_user_saved_list(self):
        all_tracks = get_all_tracks()
        yield all_tracks

    @pytest.fixture()
    def get_100_tracks_from_user_saved_list(self):
        offset = get_total_number_liked_songs() - 50
        previous, tracks = get_100_tracks(offset)
        yield tracks

    def test_create_playlist(self, create_test_playlist):
        assert create_test_playlist
        TestPlaylistChopper.sp.user_playlist_unfollow(
            TestPlaylistChopper.user_id,
            create_test_playlist.get('id')
        )

    def test_get_all_playlists(self):
        playlists = get_all_playlists()
        assert playlists

    def test_get_all_tracks(self):
        track_list = get_all_tracks()
        assert 'error' not in track_list

    def test_verify_order_by_time_added(self, get_100_tracks_from_user_saved_list):
        print(get_100_tracks_from_user_saved_list)
        assert verify_order_by_time_added(get_100_tracks_from_user_saved_list)
