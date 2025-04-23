from collections import defaultdict

def my_t9(digit_sequence):
    digit_to_char = {
        '2': 'abc', '3': 'def', '4': 'ghi',
        '5': 'jkl', '6': 'mno', '7': 'pqrs',
        '8': 'tuv', '9': 'wxyz'
    }

    words = load_words('/usr/share/dict/words')
    possible_words = set()

    def backtrack(index, path):
        if index == len(digit_sequence):
            possible_words.add(''.join(path))
            return
        for char in digit_to_char.get(digit_sequence[index], ''):
            path.append(char)
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])
    return list(filter(lambda word: word in words, possible_words))

# Пример использования
print(my_t9("22736368"))
