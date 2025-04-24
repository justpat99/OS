import gc, psutil, os, time
from utils.metadata_fetcher import threaded_fetch_tracks, create_playlist_from_tracks
process = psutil.Process(os.getpid())

def print_usage(stage: str):
    mem = process.memory_info().rss / (1024 ** 2)
    cpu = psutil.cpu_percent(interval=None)
    print(f"[{stage}] CPU: {cpu:.1f}%  RAM: {mem:.1f} MB")
    
def optimize_process():
    process = psutil.Process(os.getpid())
    try:
        process.nice(10)  # Lower priority → nice to other processes
        process.cpu_affinity([0, 1])  # Run on CPU cores 0 and 1
        print("🧠 Process scheduling optimized: Nice level set, CPU affinity adjusted.")
    except Exception as e:
        print(f"⚠️ Could not set process scheduling: {e}")

def main():
    optimize_process()
    keyword = input("Enter a mood, genre, or artist to search: ")
    
    # Step 1: Fetch tracks using threads
    print_usage("Before fetch")
    tracks = threaded_fetch_tracks(keyword, limit=10, max_workers=5)
    print_usage("After fetch")

    if not tracks:
        print("No tracks found.")
        return

    # Step 2: Display the found tracks
    print("\nTracks found:")
    for idx, t in enumerate(tracks, start=1):
        print(f"{idx}. {t['name']} — {t['artist']}")

    # Step 3: Create playlist from tracks
    create_playlist_from_tracks(tracks)
    print()
    print_usage("Before playlist creation")
    print_usage("After playlist creation")

    # Step 4: OS optimization: Free memory manually
    del tracks
    gc.collect()
    print()
    print_usage("After cleanup")

    print("\n✅ Playlist created and memory cleaned up.")

if __name__ == "__main__":
    main()