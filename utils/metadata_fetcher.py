import spotipy
from spotipy.oauth2 import SpotifyOAuth
from optimization.threaded_processor import threaded_process

# Spotify OAuth configuration
SPOTIFY_CLIENT_ID = "72474caf37cd4fd7b860f677916a9ca5"
SPOTIFY_CLIENT_SECRET = "0f6196902ccf47b5bc2a41c7fb56854e"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public playlist-modify-private"

# Initialize Spotify client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache"
))


def threaded_fetch_tracks(query: str, limit: int = 10, max_workers: int = 5):
    """
    Search for tracks matching the query in parallel using threads.
    Returns a list of track dicts with 'id', 'name', 'artist'.
    """
    def search_task(offset):
        results = sp.search(q=query, type='track', limit=1, offset=offset)
        items = results.get('tracks', {}).get('items', [])
        if items:
            item = items[0]
            return {
                'id': item['id'],
                'name': item['name'],
                'artist': item['artists'][0]['name']
            }
        return None

    offsets = list(range(limit))
    results = threaded_process(search_task, offsets, max_workers=max_workers)
    # Filter out any None results
    return [track for track in results if track]


def create_playlist_from_tracks(tracks: list, playlist_name: str = None, public: bool = False):
    """
    Create a Spotify playlist from a list of track dicts.
    Each track dict must contain 'id'.
    """
    user_id = sp.current_user()['id']
    if not playlist_name:
        playlist_name = "Generated Playlist"

    # Create playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=public)
    track_uris = [f"spotify:track:{t['id']}" for t in tracks]

    # Add tracks in batches of 100 (Spotify limit)
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris[i:i+100])

    print(f"✅ Playlist '{playlist_name}' created with {len(track_uris)} tracks!")
    return playlist['id']
