import asyncio
import subprocess
import sys
import time


def run_comparison():
    test_cases = [10, 50, 100]
    results = []

    for num_cats in test_cases:
        print(f"\n{'=' * 50}")
        print(f"Testing with {num_cats} cats")
        print(f"{'=' * 50}")

        # Запуск асинхронной версии
        print("Running async version...")
        start_time = time.time()
        result = subprocess.run([sys.executable, "async_cats.py"],
                                input=str(num_cats), text=True, capture_output=True)
        async_time = time.time() - start_time
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        # Запуск threaded версии
        print("Running threaded version...")
        start_time = time.time()
        result = subprocess.run([sys.executable, "threaded_cats.py"],
                                input=str(num_cats), text=True, capture_output=True)
        threaded_time = time.time() - start_time
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        # Запуск multiprocess версии
        print("Running multiprocess version...")
        start_time = time.time()
        result = subprocess.run([sys.executable, "multiprocess_cats.py"],
                                input=str(num_cats), text=True, capture_output=True)
        process_time = time.time() - start_time
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        results.append({
            'num_cats': num_cats,
            'async': async_time,
            'threaded': threaded_time,
            'multiprocess': process_time
        })

    # Вывод результатов
    print(f"\n{'=' * 60}")
    print("COMPARISON RESULTS:")
    print(f"{'=' * 60}")
    print(f"{'Cats':<10} {'Async (s)':<12} {'Threaded (s)':<12} {'Multiprocess (s)':<15}")
    print(f"{'-' * 60}")

    for result in results:
        print(
            f"{result['num_cats']:<10} {result['async']:<12.2f} {result['threaded']:<12.2f} {result['multiprocess']:<15.2f}")


if __name__ == "__main__":
    run_comparison()