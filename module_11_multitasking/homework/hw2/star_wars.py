import requests
import time
import threading
import sqlite3
from datetime import datetime

def create_db():
    conn = sqlite3.connect('star_wars.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS characters
                 (name TEXT, gender TEXT, birth_year TEXT)''')
    conn.commit()
    conn.close()

def fetch_character_sync(url):
    response = requests.get(url)
    data = response.json()
    return {
        'name': data['name'],
        'gender': data['gender'],
        'birth_year': data['birth_year']
    }

def save_character(character):
    conn = sqlite3.connect('star_wars.db')
    c = conn.cursor()
    c.execute("INSERT INTO characters VALUES (?, ?, ?)", 
              (character['name'], character['gender'], character['birth_year']))
    conn.commit()
    conn.close()

def sync_version():
    start = time.time()
    base_url = "https://swapi.dev/api/people/"
    urls = [f"{base_url}{i}/" for i in range(1, 21)]
    
    for url in urls:
        try:
            character = fetch_character_sync(url)
            save_character(character)
        except:
            continue
    
    end = time.time()
    print(f"Sync version took {end - start:.2f} seconds")

def fetch_character_thread(url, results, index):
    try:
        response = requests.get(url)
        data = response.json()
        results[index] = {
            'name': data['name'],
            'gender': data['gender'],
            'birth_year': data['birth_year']
        }
    except:
        results[index] = None

def threaded_version():
    start = time.time()
    base_url = "https://swapi.dev/api/people/"
    urls = [f"{base_url}{i}/" for i in range(1, 21)]
    results = [None] * len(urls)
    threads = []
    
    for i, url in enumerate(urls):
        thread = threading.Thread(target=fetch_character_thread, args=(url, results, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    for character in results:
        if character:
            save_character(character)
    
    end = time.time()
    print(f"Threaded version took {end - start:.2f} seconds")

if __name__ == "__main__":
    create_db()
    sync_version()
    threaded_version()
