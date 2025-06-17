import subprocess

def process_count(username: str) -> int:
    cmd = f"ps -u {username} | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # Вычитаем 1, чтобы исключить заголовок
    return int(result.stdout.strip()) - 1

def total_memory_usage(root_pid: int) -> float:
    # Получаем все PID процессов в дереве
    cmd = f"pgrep -P {root_pid} | xargs echo && echo {root_pid}"
    pids = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Получаем суммарное потребление памяти
    cmd = f"ps -o %mem -p {pids.stdout.replace(' ', ',')} | awk '{{s+=$1}} END {{print s}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return float(result.stdout.strip())

if __name__ == '__main__':
    print(f"Processes for current user: {process_count('username')}")
    print(f"Total memory usage: {total_memory_usage(1)}%")
