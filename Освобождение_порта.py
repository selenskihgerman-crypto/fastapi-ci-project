import os
import signal
import subprocess
import time

def free_port_and_run_server(port: int, run_server_func, *args, **kwargs):
    """
    Пытается запустить сервер на порту. Если порт занят — завершает процесс, который занимает порт, и пробует снова.
    run_server_func — функция, запускающая сервер.
    """
    def is_port_busy():
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        return lines[1:] if len(lines) > 1 else []

    while True:
        busy = is_port_busy()
        if not busy:
            try:
                return run_server_func(*args, **kwargs)
            except OSError as e:
                # если всё же не удалось — возможно, гонка процессов
                time.sleep(0.5)
                continue
        else:
            # lsof выводит: COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
            # Нужно взять PID (второй столбец)
            for line in busy:
                pid = int(line.split()[1])
                try:
                    os.kill(pid, signal.SIGTERM)
                    print(f"Процесс {pid} остановлен для освобождения порта {port}")
                except Exception as e:
                    print(f"Не удалось завершить процесс {pid}: {e}")
            time.sleep(0.5)  # Даем время системе освободить порт
