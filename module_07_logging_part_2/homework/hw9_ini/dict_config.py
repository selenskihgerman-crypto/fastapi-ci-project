# TODO переписать реализацию ini-файла в формате dict-конфигурации.

# 3. Как применить dict-конфиг в коде Python?

import logging.config

# Импортируй LOGGING_CONFIG из своего файла, например:
# from my_logging_dict import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

# Пример использования логгера
logger = logging.getLogger("app")
logger.info("Hello, лог из файла!")
