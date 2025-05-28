# Дополнение к седьмой задаче

'filters': {
    'ascii': {
        '()': 'ascii_filter.AsciiFilter'
    }
},
'handlers': {
    'console': {
        # ...
        'filters': ['ascii'],
    },
    # ...
}

