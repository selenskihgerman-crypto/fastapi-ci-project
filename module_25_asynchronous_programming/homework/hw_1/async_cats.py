import aiohttp
import asyncio
import os
import time


async def download_cat(session, url, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                # Используем стандартный open вместо aiofiles
                with open(save_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"Downloaded: {save_path}")
            else:
                print(f"Failed to download {url}: Status {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


async def download_cats_async(num_cats):
    os.makedirs('cats_async', exist_ok=True)
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_cats):
            url = f"https://cataas.com/cat?type=sq&cache_buster={i}"
            save_path = f"cats_async/cat_{i}.jpg"
            task = asyncio.create_task(download_cat(session, url, save_path))
            tasks.append(task)

        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Async downloaded {num_cats} cats in {end_time - start_time:.2f} seconds")
    return end_time - start_time


if __name__ == "__main__":
    num_cats = int(input("How many cats to download? "))
    asyncio.run(download_cats_async(num_cats))