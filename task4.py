import json
from collections import Counter

def analyze_logs(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    levels_count = Counter()
    hour_count = Counter()
    dog_count = 0
    warning_words = []

    for line in lines:
        log = json.loads(line)
        levels_count[log['level']] += 1
        hour = log['time'][:2]
        hour_count[hour] += 1
        if 'dog' in log['message'].lower():
            dog_count += 1
        if log['level'] == 'WARNING':
            warning_words.extend(log['message'].split())

    most_common_warning = Counter(warning_words).most_common(1)

    return levels_count, hour_count.most_common(1), dog_count, most_common_warning

# Пример использования
results = analyze_logs('skillbox_json_messages.log')
