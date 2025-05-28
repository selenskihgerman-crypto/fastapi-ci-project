# Задача 5. Ротация логов (TimedRotatingFileHandler для utils)

'handlers': {
    # ...
    'utils_rotating': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'formatter': 'full',
        'filename': 'utils.log',
        'when': 'h',
        'interval': 1,
        'backupCount': 10,
        'level': 'INFO'
    }
},
'loggers': {
    'utils': {
        'handlers': ['utils_rotating'],
        'level': 'INFO',
        'propagate': False
    }
}
# Только для utils, только INFO и выше.

