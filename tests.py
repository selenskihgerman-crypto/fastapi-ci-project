import unittest
from app import app

class TestCodeExec(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_successful_code(self):
        resp = self.client.post('/execute', data={'code': "print('hi')", 'timeout': 3})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('hi', resp.get_json()['output'])

    def test_timeout(self):
        resp = self.client.post('/execute', data={'code': "import time; time.sleep(5)", 'timeout': 1})
        self.assertEqual(resp.status_code, 408)
        self.assertIn('Timeout', resp.get_json()['error'])

    def test_invalid_data(self):
        resp = self.client.post('/execute', data={'code': '', 'timeout': 100})
        self.assertEqual(resp.status_code, 400)

    def test_shell_injection(self):
        # Должно быть безопасно, не shell=True
        resp = self.client.post('/execute', data={'code': 'print()"; echo "hacked', 'timeout': 3})
        self.assertNotIn('hacked', resp.get_json().get('output', '') + resp.get_json().get('stderr', ''))

if __name__ == '__main__':
    unittest.main()
