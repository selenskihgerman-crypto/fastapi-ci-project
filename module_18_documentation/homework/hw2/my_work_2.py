# Класс для тестирования скорости API

import time
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import partial


class ApiBenchmark:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def make_request(self, use_session=False):
        """Выполняет один запрос к API"""
        if use_session:
            return self.session.get(f"{self.base_url}/api/books/")
        else:
            return requests.get(f"{self.base_url}/api/books/")

    def run_benchmark(self, num_requests, use_session=False, use_threads=False):
        """Запускает тестирование с заданными параметрами"""
        start_time = time.time()

        if use_threads:
            with ThreadPoolExecutor(max_workers=10) as executor:
                func = partial(self.make_request, use_session)
                list(executor.map(func, range(num_requests)))
        else:
            for _ in range(num_requests):
                self.make_request(use_session)

        elapsed_time = time.time() - start_time
        return elapsed_time


# Пример использования
if __name__ == "__main__":
    benchmark = ApiBenchmark("http://localhost:5000")

    # Тестируем разные комбинации параметров
    test_cases = [
        (10, False, False),
        (10, True, False),
        (10, False, True),
        (10, True, True),
        (100, False, False),
        (100, True, False),
        (100, False, True),
        (100, True, True),
        (1000, False, False),
        (1000, True, False),
        (1000, False, True),
        (1000, True, True),
    ]

    results = {}
    for num, use_sess, use_thr in test_cases:
        key = f"n={num}, sess={use_sess}, thr={use_thr}"
        results[key] = benchmark.run_benchmark(num, use_sess, use_thr)

    for test, time_taken in results.items():
        print(f"{test}: {time_taken:.2f} сек")