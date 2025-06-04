# Задача 7. Только ASCII (собственный Filter)

import logging

class AsciiFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().isascii()
