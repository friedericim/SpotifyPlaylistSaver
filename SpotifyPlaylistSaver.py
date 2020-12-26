import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser

def get_playlist_tracks(playlist):
    tracks = playlist["items"]
    while playlist["next"]:
        playlist = sp.next(playlist)
        tracks.extend(playlist["items"])
    return tracks


def track_is_in_tracks(track_id, tracks):
    for current_track in tracks:
        if track_id == current_track["track"]["id"]:
            return True
    return False


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b696110c000e43b895b83333bdd08c2d",
                                               client_secret="64f87b67343045039906b15abe0ffdb5",
                                               redirect_uri="http://localhost:8080",
                                               scope="user-library-read playlist-modify-private playlist-read-private",
                                               cache_path = '.spotipyoauthcache'))

playlists = sp.current_user_playlists()

#Read Playlist ids from config-file
config = configparser.ConfigParser()
try:
    config.read("./playlist.config")
    source_playlist_id = config.get("CONFIG", "source_playlist_id")
    target_playlist_id = config.get("CONFIG", "target_playlist_id")
    
except FileNotFoundError:
    print("Config-file not found!")
    exit()

try:
    source_playlist_tracks = sp.playlist_tracks(source_playlist_id)["items"]
    source_playlist_track_ids = []
    target_playlist_tracks = get_playlist_tracks(sp.playlist_tracks(target_playlist_id))

    for track in source_playlist_tracks:
        track_id = track["track"]["id"]
        
        if not track_is_in_tracks(track_id, target_playlist_tracks):
            source_playlist_track_ids.append(track["track"]["id"])
        else:
            print("not added!")

    if source_playlist_track_ids:
        sp.playlist_add_items(target_playlist_id, source_playlist_track_ids)
        
except:
    print("Something went wrong!")
