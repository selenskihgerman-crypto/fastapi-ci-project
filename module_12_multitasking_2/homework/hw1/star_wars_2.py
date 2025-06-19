# Задание 1.

import requests
import sqlite3
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool


def create_db():
    conn = sqlite3.connect('star_wars.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS characters
                      (name TEXT, age INTEGER, gender TEXT)''')
    conn.commit()
    conn.close()


def get_character_data(character_id):
    response = requests.get(f'https://swapi.dev/api/people/{character_id}/')
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data.get('name'),
            'age': data.get('birth_year'),
            'gender': data.get('gender')
        }
    return None


def save_to_db(character_data):
    if character_data:
        conn = sqlite3.connect('star_wars.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO characters VALUES (?, ?, ?)",
                       (character_data['name'], character_data['age'], character_data['gender']))
        conn.commit()
        conn.close()


def process_pool_version():
    start_time = time.time()
    create_db()

    with Pool(4) as pool:  # Используем 4 процесса
        results = pool.map(get_character_data, range(1, 21))
        for result in results:
            save_to_db(result)

    print(f"Process Pool time: {time.time() - start_time:.2f} seconds")


def thread_pool_version():
    start_time = time.time()
    create_db()

    with ThreadPool(20) as pool:  # Используем 20 потоков
        results = pool.map(get_character_data, range(1, 21))
        for result in results:
            save_to_db(result)

    print(f"Thread Pool time: {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    process_pool_version()
    thread_pool_version()
