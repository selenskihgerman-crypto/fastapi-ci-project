import re

def measure_time_from_logs(file_path):
    times = []

    with open(file_path, 'r') as f:
        for line in f:
            if "Enter measure_me" in line:
                start_time = float(re.search(r'(\d+\.\d+)', line).group(1))
            elif "Leave measure_me" in line:
                end_time = float(re.search(r'(\d+\.\d+)', line).group(1))
                times.append(end_time - start_time)

    return sum(times) / len(times) if times else 0

# Пример использования
average_time = measure_time_from_logs('logs.txt')  # Укажите свой файл лог
