import logging

# Настройка логгера
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
file_handler = logging.FileHandler('stderr.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Пример использования логгера
logger.info('Это информационное сообщение')
