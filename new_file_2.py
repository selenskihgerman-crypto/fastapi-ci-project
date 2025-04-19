import unittest
from your_module import decoder  # замените на свою функцию

class TestDecoder(unittest.TestCase):
    def test_no_dots(self):
        """абра-кадабра -> абра-кадабра"""
        self.assertEqual(decoder('абра-кадабра'), 'абра-кадабра')

    def test_double_dot_cases(self):
        """Проверки с двумя точками"""
        cases = [
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
        ]
        for inp, expected in cases:
            with self.subTest(inp=inp):
                self.assertEqual(decoder(inp), expected)

    def test_triple_dot_cases(self):
        """Проверки с тремя и более точками"""
        cases = [
            ('абрау...-кадабра', 'абра-кадабра'),
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('.', ''),
            ('1.......................', ''),
        ]
        for inp, expected in cases:
            with self.subTest(inp=inp):
                self.assertEqual(decoder(inp), expected)
