# from utils.metadata_fetcher import search_tracks_by_keyword

# def main():
#     keyword = input("Enter a mood, genre, or artist to search: ")
#     results = search_tracks_by_keyword(keyword)

#     if results:
#         print("\nFound tracks:")
#         for i, track in enumerate(results, start=1):
#             print(f"{i}. {track['name']} by {track['artist']}")
#     else:
#         print("No tracks found for your search.")
        
# if __name__ == "__main__":
#     main()

# from utils.metadata_fetcher import search_tracks_by_keyword, create_playlist

# def main():
#     keyword = input("Enter a mood, genre, or artist to search: ")

#     # 1. Search for tracks
#     search_results = search_tracks_by_keyword(keyword)

#     if not search_results:
#         print("No tracks found.")
#         return

#     # 2. Show results
#     print("\nFound tracks:")
#     for idx, track in enumerate(search_results, 1):
#         print(f"{idx}. {track['name']} by {track['artist']}")

#     # 3. Extract track IDs
#     track_ids = [track['id'] for track in search_results]

#     # 4. Create playlist and add tracks
#     playlist_name = f"{keyword.capitalize()} Vibes Playlist"
#     playlist_id = create_playlist(playlist_name, track_ids)

#     if playlist_id:
#         print(f"\nPlaylist '{playlist_name}' created successfully!")
#     else:
#         print("\nFailed to create playlist.")

# if __name__ == "__main__":
#     main()

# import gc
# from utils.metadata_fetcher import threaded_fetch_tracks, create_playlist_from_tracks

# def main():
#     keyword = input("Enter a mood, genre, or artist to search: ")
    
#     # Step 1: Fetch tracks using threads
#     tracks = threaded_fetch_tracks(keyword, limit=10, max_workers=5)

#     if not tracks:
#         print("No tracks found.")
#         return

#     # Step 2: Display the found tracks
#     print("\nTracks:")
#     for t in tracks:
#         print(f"{t['name']} — {t['artist']}")

#     # Step 3: Create playlist from tracks
#     create_playlist_from_tracks(tracks)

#     # Step 4: Memory management
#     del tracks
#     gc.collect()

#     print("\n✅ Done! Memory cleaned up.")

# if __name__ == "__main__":
#     main()

# from utils.playlist_saver import save_playlist_async

# # … once you have your `playlist_data` object (list or dict):
# save_playlist_async(playlist_name, playlist_data)
# print("Saving playlist in background…")

import gc
from utils.metadata_fetcher import threaded_fetch_tracks, create_playlist_from_tracks

def main():
    keyword = input("Enter a mood, genre, or artist to search: ")
    
    # Step 1: Fetch tracks using threads
    tracks = threaded_fetch_tracks(keyword, limit=10, max_workers=5)

    if not tracks:
        print("No tracks found.")
        return

    # Step 2: Display the found tracks
    print("\nTracks found:")
    for idx, t in enumerate(tracks, start=1):
        print(f"{idx}. {t['name']} — {t['artist']}")

    # Step 3: Create playlist from tracks
    create_playlist_from_tracks(tracks)

    # Step 4: OS optimization: Free memory manually
    del tracks
    gc.collect()

    print("\n✅ Playlist created and memory cleaned up.")

if __name__ == "__main__":
    main()
