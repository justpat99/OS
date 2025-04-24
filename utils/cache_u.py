import os, json, gzip
from hashlib import sha1

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(key: str):
    filename = sha1(key.encode()).hexdigest() + ".json.gz"
    return os.path.join(CACHE_DIR, filename)

def load_from_cache(key: str):
    path = get_cache_path(key)
    if os.path.exists(path):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_to_cache(key: str, data):
    path = get_cache_path(key)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(data, f)
