import multiprocessing

def parallel_fetch(fetch_function, keywords, max_processes=4):
    """
    Run fetch_function on a list of keywords in parallel using multiprocessing.
    """
    with multiprocessing.Pool(processes=max_processes) as pool:
        results = pool.map(fetch_function, keywords)

    # Flatten list if needed
    flat_results = [item for sublist in results for item in sublist if item]

    return flat_results
