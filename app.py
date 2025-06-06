# Задача 1. Добавляем логирование

import logging
from utils import add, subtract

logger = logging.getLogger("app")

def main():
    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))

        result_add = add(a, b)
        logger.info(f"Сложение: {a} + {b} = {result_add}")

        result_sub = subtract(a, b)
        logger.info(f"Вычитание: {a} - {b} = {result_sub}")

    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
