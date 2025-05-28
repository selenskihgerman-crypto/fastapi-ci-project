# Задача 3. Многоуровневый обработчик (debug/error в разные файлы)

import logging

def configure_logging():
    # ... (предыдущий код)

    debug_handler = logging.FileHandler('calc_debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    error_handler = logging.FileHandler('calc_error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger = logging.getLogger()
    # Очищаем handlers, чтобы не было дублей:
    logger.handlers.clear()
    logger.addHandler(handler)  # stdout
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
