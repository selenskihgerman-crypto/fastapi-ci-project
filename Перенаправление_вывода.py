import sys
import traceback

class Redirect:
    def __init__(self, *, stdout=None, stderr=None):
        self.stdout = stdout
        self.stderr = stderr

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        if self.stdout:
            sys.stdout = self.stdout
        if self.stderr:
            sys.stderr = self.stderr

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Если перенаправляли stderr и есть исключение
        if self.stderr and exc_type is not None:
            # Записываем информацию об исключении в текущий поток ошибок
            sys.stderr.write(traceback.format_exc())
        
        # Возвращаем потоки обратно
        if self.stdout:
            sys.stdout = self.old_stdout
        if self.stderr:
            sys.stderr = self.old_stderr
        
        # Если перенаправляли stderr, подавляем исключение
        if self.stderr and exc_type is not None:
            return True  # подавляем исключение (оно уже записано в файл/поток)
