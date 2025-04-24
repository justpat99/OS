# import time
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from optimization.threaded_processor import threaded_process  # ต้องทำให้ฟังก์ชันนี้พร้อมใช้งาน

# # Set up Spotify client
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id="72474caf37cd4fd7b860f677916a9ca5",
#     client_secret="0f6196902ccf47b5bc2a41c7fb56854e",
#     redirect_uri="http://127.0.0.1:8888/callback",
#     scope="playlist-modify-public playlist-modify-private",
#     cache_path=".cache"
# ))

# # ฟังก์ชันการค้นหาเพลงแบบไม่ใช้ Thread (ทำงานทีละเพลง)
# def fetch_tracks_sequential(query, limit=10):
#     tracks = []
#     for i in range(limit):
#         results = sp.search(q=query, type='track', limit=1, offset=i)
#         items = results.get('tracks', {}).get('items', [])
#         if items:
#             tracks.append(items[0])
#     return tracks

# # ฟังก์ชันการค้นหาเพลงแบบใช้ Thread (ทำงานพร้อมกันหลายเพลง)
# def fetch_single_track(i, query):
#     results = sp.search(q=query, type='track', limit=1, offset=i)
#     items = results.get('tracks', {}).get('items', [])
#     if items:
#         return items[0]
#     return None

# def fetch_tracks_threaded(query, limit=10):
#     return threaded_process(lambda i: fetch_single_track(i, query), limit)

# # ฟังก์ชันหลักที่ใช้ในการทดสอบ
# if __name__ == "__main__":
#     keyword = input("Enter a keyword to search for tracks: ")
#     limit = 10  # จำนวนเพลงที่ต้องการค้นหา

#     # ทดสอบการค้นหาผ่านการทำงานแบบไม่ใช้ Thread
#     start_time = time.time()
#     tracks_sequential = fetch_tracks_sequential(keyword, limit)
#     end_time = time.time()
#     print(f"Fetched {len(tracks_sequential)} tracks (sequential).")
#     print(f"Time taken WITHOUT threading: {end_time - start_time:.2f} seconds")

#     # ทดสอบการค้นหาผ่านการทำงานแบบใช้ Thread
#     start_time = time.time()
#     tracks_threaded = fetch_tracks_threaded(keyword, limit)
#     end_time = time.time()
#     print(f"Fetched {len([t for t in tracks_threaded if t])} tracks (threaded).")
#     print(f"Time taken WITH threading: {end_time - start_time:.2f} seconds")

import time
from utils.metadata_fetcher import threaded_fetch_tracks
from optimization.multiprocessing_handler import parallel_fetch

# Sequential version
def sequential_fetch(keywords):
    results = []
    for keyword in keywords:
        result = threaded_fetch_tracks(keyword, limit=5, max_workers=1)
        results.extend(result)
    return results

# Threaded version (still runs sequentially per keyword, but with threads inside)
def threaded_version(keywords):
    results = []
    for keyword in keywords:
        result = threaded_fetch_tracks(keyword, limit=5, max_workers=5)
        results.extend(result)
    return results

# Parallel version (multiple processes, each runs single-threaded)
def fetch_tracks_for_keyword(keyword):
    from utils.metadata_fetcher import threaded_fetch_tracks
    return threaded_fetch_tracks(keyword, limit=5, max_workers=1)

# Parallel + threaded version
def parallel_threaded_version(keywords):
    return parallel_fetch(fetch_tracks_for_keyword, keywords, max_processes=4)

# Benchmark runner
def run_benchmark(keywords):
    print("\n--- Benchmarking with keywords:", keywords)

    # V1: Sequential
    start = time.time()
    sequential_fetch(keywords)
    print("⏱️ Sequential:         {:.2f} sec".format(time.time() - start))

    # V2: Threaded
    start = time.time()
    threaded_version(keywords)
    print("⏱️ Threaded:           {:.2f} sec".format(time.time() - start))

    # V3: Parallel
    start = time.time()
    parallel_fetch(fetch_tracks_for_keyword, keywords, max_processes=4)
    print("⏱️ Parallel:           {:.2f} sec".format(time.time() - start))

    # V4: Parallel + Threaded
    start = time.time()
    parallel_threaded_version(keywords)
    print("⏱️ Parallel+Threaded:  {:.2f} sec".format(time.time() - start))


if __name__ == "__main__":
    keywords = ["pop", "lofi", "justin bieber", "ed sheeran"]
    run_benchmark(keywords)
