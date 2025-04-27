"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
from collections import Counter, defaultdict

levels = Counter()
hours = Counter()
critical_5_20 = 0
dog_count = 0
warning_words = Counter()

with open("skillbox_json_messages.log") as f:
    for line in f:
        data = json.loads(line)
        levels[data["level"]] += 1
        hour = data["time"][:2]
        hours[hour] += 1
        if (data["level"] == "CRITICAL" and
            "05:00:00" <= data["time"] <= "05:20:00"):
            critical_5_20 += 1
        if "dog" in data["message"].lower():
            dog_count += 1
        if data["level"] == "WARNING":
            for word in data["message"].split():
                warning_words[word.lower()] += 1

print("Messages per level:", levels)
print("Most logs in hour:", hours.most_common(1))
print("CRITICAL logs 05:00:00-05:20:00:", critical_5_20)
print("Messages with 'dog':", dog_count)
print("Most frequent WARNING word:", warning_words.most_common(1))
