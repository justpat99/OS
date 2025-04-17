import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="72474caf37cd4fd7b860f677916a9ca5",
    client_secret="0f6196902ccf47b5bc2a41c7fb56854e",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public playlist-modify-private"
))

def create_playlist_from_tracks(tracks, playlist_name="Generated Playlist"):
    user_id = sp.current_user()["id"]

    # Create a new playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = playlist["id"]

    # Extract track URIs
    track_uris = [track["uri"] for track in tracks if "uri" in track]

    # Add tracks to the new playlist
    sp.playlist_add_items(playlist_id, track_uris)

    print(f"✅ Playlist '{playlist_name}' created with {len(track_uris)} tracks!")
