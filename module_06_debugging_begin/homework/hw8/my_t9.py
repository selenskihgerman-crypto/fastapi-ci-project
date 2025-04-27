"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
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
