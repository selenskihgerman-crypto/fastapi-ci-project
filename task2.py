import re

def load_words(file_path):
    with open(file_path, 'r') as f:
        return set(word.strip().lower() for word in f if len(word.strip()) > 4)

def is_strong_password(password, word_set):
    words_in_password = re.findall(r'\b\w+\b', password.lower())
    return not any(word in word_set for word in words_in_password)

# Пример использования
words = load_words('/usr/share/dict/words')
print(is_strong_password("MySecurePassword", words))
