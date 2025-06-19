# Задание 4.

import threading
import time
import requests
from queue import Queue
import datetime

log_queue = Queue()
stop_event = threading.Event()

def worker(worker_id):
    start_time = time.time()
    while time.time() - start_time < 20 and not stop_event.is_set():
        timestamp = int(time.time())
        try:
            response = requests.get(f'http://127.0.0.1:8080/timestamp/{timestamp}')
            date = response.text
            log_queue.put((timestamp, date))
        except requests.RequestException:
            pass
        time.sleep(1)

def logger():
    with open('sorted_logs.txt', 'w') as f:
        while not stop_event.is_set() or not log_queue.empty():
            if not log_queue.empty():
                timestamp, date = log_queue.get()
                f.write(f"{timestamp} {date}\n")
                f.flush()
            time.sleep(0.1)

def main():
    # Запускаем поток для записи логов
    logger_thread = threading.Thread(target=logger)
    logger_thread.start()
    
    # Запускаем 10 рабочих потоков с интервалом в 1 секунду
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(1)
    
    # Ждем завершения всех рабочих потоков
    for t in threads:
        t.join()
    
    # Даем логгеру время завершить запись
    stop_event.set()
    logger_thread.join()

if __name__ == '__main__':
    main()
