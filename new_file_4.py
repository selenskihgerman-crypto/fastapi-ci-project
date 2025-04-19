import unittest
import datetime
from your_module import Person  # замените на свою реализацию

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.p = Person("Иван", 1990, "Москва")

    def test_get_name(self):
        self.assertEqual(self.p.get_name(), "Иван")

    def test_set_name(self):
        self.p.set_name("Петр")
        self.assertEqual(self.p.name, "Петр")

    def test_set_address(self):
        self.p.set_address("Питер")
        self.assertEqual(self.p.address, "Питер")

    def test_get_address(self):
        self.assertEqual(self.p.get_address(), "Москва")

    def test_get_age(self):
        now = datetime.datetime.now()
        self.p.yob = now.year - 30
        self.assertEqual(self.p.get_age(), 30)

    def test_is_homeless(self):
        self.assertFalse(self.p.is_homeless())
        self.p.address = None
        self.assertTrue(self.p.is_homeless())
