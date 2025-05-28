# Задача 4. dict-конфигурация (вынести в отдельный shared_logging_dict.py)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'full',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
        'debug_file': {
            'class': 'logging.FileHandler',
            'formatter': 'full',
            'level': 'DEBUG',
            'filename': 'calc_debug.log'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'formatter': 'full',
            'level': 'ERROR',
            'filename': 'calc_error.log'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'debug_file', 'error_file']
    },
}
