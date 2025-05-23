import re
from bisect import bisect_left

def load_words(path="/usr/share/dict/words"):
    with open(path) as f:
        words = [line.strip().lower() for line in f if len(line.strip()) > 4]
    words.sort()
    return words

EN_WORDS = load_words()

def contains_word(password, word_list):
    password_lower = password.lower()
    for i in range(len(password_lower)):
        for j in range(i+5, len(password_lower)+1):
            candidate = password_lower[i:j]
            idx = bisect_left(word_list, candidate)
            if idx < len(word_list) and word_list[idx] == candidate:
                return True
    return False

def is_strong_password(password):
    return not contains_word(password, EN_WORDS)
