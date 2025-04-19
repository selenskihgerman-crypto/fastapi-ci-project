import unittest
from your_flask_app import app, storage  # замените на свой модуль

class TestFinanceApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Заполняем storage начальными данными
        storage.clear()
        storage.update({
            '20240610': 100,
            '20240611': 200,
        })
        cls.client = app.test_client()

    def test_add_valid(self):
        """Проверяем успешное добавление"""
        resp = self.client.post('/add/', json={'date': '20240612', 'amount': 300})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('20240612', storage)

    def test_add_invalid_date(self):
        """Проверяем обработку неправильной даты"""
        with self.assertRaises(Exception):
            self.client.post('/add/', json={'date': '12-06-2024', 'amount': 100})

    def test_calculate_day(self):
        """Проверяем расчет за день"""
        resp = self.client.get('/calculate/?date=20240610')
        self.assertIn('100', resp.get_data(as_text=True))

    def test_calculate_period(self):
        """Проверяем расчет за период"""
        resp = self.client.get('/calculate/?from_date=20240610&to_date=20240611')
        self.assertIn('300', resp.get_data(as_text=True))

    def test_calculate_empty_storage(self):
        """Проверяем расчет, если storage пустой"""
        storage.clear()
        resp = self.client.get('/calculate/?date=20240610')
        self.assertIn('0', resp.get_data(as_text=True))
