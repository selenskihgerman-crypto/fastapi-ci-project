# Задача 2. ООП-конфигурация (basicConfig + Formatter + stdout)

import logging
import sys

def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    handler.setFormatter(formatter)
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[handler]
    )
