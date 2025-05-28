# Дополнение к первой задаче

import logging
logger = logging.getLogger("utils")

def add(x, y):
    logger.debug(f"add({x}, {y})")
    return x + y

def subtract(x, y):
    logger.debug(f"subtract({x}, {y})")
    return x - y
