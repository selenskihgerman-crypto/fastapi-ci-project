import unittest
from freezegun import freeze_time
from your_module import get_username_with_weekdate  # замените на свою функцию

class TestUsernameWithWeekDate(unittest.TestCase):
    WEEKDAYS = [
        ("Понедельника", "2024-06-10"), # понедельник
        ("Вторника", "2024-06-11"),
        ("Среды", "2024-06-12"),
        ("Четверга", "2024-06-13"),
        ("Пятницы", "2024-06-14"),
        ("Субботы", "2024-06-15"),
        ("Воскресенья", "2024-06-16"),
    ]

    def test_username_contains_correct_weekday(self):
        """Проверка корректного дня недели в username"""
        for weekday, date in self.WEEKDAYS:
            with self.subTest(weekday=weekday):
                with freeze_time(date):
                    result = get_username_with_weekdate()
                    self.assertIn(weekday, result)

    def test_good_wish_in_username(self):
        """Проверка корректности пожелания хорошего дня"""
        for weekday, date in self.WEEKDAYS:
            with self.subTest(weekday=weekday):
                with freeze_time(date):
                    username = f'Хорошей {weekday.lower()}'
                    result = get_username_with_weekdate(username=username)
                    self.assertIn(weekday, result)
                    self.assertIn('Хорошей', result)
