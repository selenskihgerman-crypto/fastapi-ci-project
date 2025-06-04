# Задача 5. Ротация логов.

import logging
from logging.handlers import TimedRotatingFileHandler

# Создаем логгер для utils
logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)  # Только INFO и выше

# Создаем обработчик с ротацией по времени
handler = TimedRotatingFileHandler(
    'utils.log',  # Имя файла
    when='H',     # Ротация по часам
    interval=10,  # Каждые 10 часов
    backupCount=1, # Храним только 1 резервную копию (текущий + предыдущий)
)

# Настраиваем формат сообщений
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)

# Пример использования
logger.info('Это информационное сообщение')
logger.warning('Это предупреждение')
logger.debug('Это сообщение отладки - не должно попасть в лог')  # Не попадет в лог
