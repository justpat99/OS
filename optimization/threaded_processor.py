from concurrent.futures import ThreadPoolExecutor

def threaded_process(task_function, iterable, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task_function, item) for item in iterable]
        for future in futures:
            result = future.result()
            results.append(result)
    return results
