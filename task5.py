import re
from datetime import datetime

def parse_time(s):
    # Ожидаемый формат: HH:MM:SS,mmm
    return datetime.strptime(s, "%H:%M:%S,%f")

with open("measure_me.log") as f:
    lines = [line for line in f if "Enter measure_me" in line or "Leave measure_me" in line]

times = []
for i in range(0, len(lines), 2):
    enter = re.search(r"(\d{2}:\d{2}:\d{2},\d{3})", lines[i]).group(1)
    leave = re.search(r"(\d{2}:\d{2}:\d{2},\d{3})", lines[i+1]).group(1)
    t1, t2 = parse_time(enter), parse_time(leave)
    times.append((t2 - t1).total_seconds())

print("Average execution time:", sum(times)/len(times), "seconds")
