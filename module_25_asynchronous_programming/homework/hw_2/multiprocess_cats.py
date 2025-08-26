import requests
import multiprocessing
import os
import time


def download_cat(args):
    url, save_path = args
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def download_cats_multiprocess(num_cats):
    os.makedirs('cats_processes', exist_ok=True)
    start_time = time.time()

    tasks = []
    for i in range(num_cats):
        url = f"https://cataas.com/cat?type=sq&cache_buster={i}"
        save_path = f"cats_processes/cat_{i}.jpg"
        tasks.append((url, save_path))

    with multiprocessing.Pool(processes=min(10, num_cats)) as pool:
        pool.map(download_cat, tasks)

    end_time = time.time()
    print(f"Multiprocess downloaded {num_cats} cats in {end_time - start_time:.2f} seconds")
    return end_time - start_time


if __name__ == "__main__":
    num_cats = int(input("How many cats to download? "))
    download_cats_multiprocess(num_cats)