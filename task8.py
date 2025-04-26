T9 = {
    '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
    '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
}

def digits_to_pattern(digits):
    return '^' + ''.join(f"[{T9[d]}]" for d in digits) + '$'

import re

def my_t9(digits, word_file="/usr/share/dict/words"):
    pattern = re.compile(digits_to_pattern(digits), re.IGNORECASE)
    words = []
    with open(word_file) as f:
        for word in f:
            word = word.strip()
            if len(word) == len(digits) and pattern.match(word):
                words.append(word.lower())
    return words

# Пример: my_t9('22736368') -> ['basement']
