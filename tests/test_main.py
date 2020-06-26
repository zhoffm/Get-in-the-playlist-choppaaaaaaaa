import pytest
import spotipy
import logging
from spotipy.oauth2 import SpotifyOAuth
from main import create_playlist, get_all_playlists, get_all_tracks

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
