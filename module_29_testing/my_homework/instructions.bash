# 1. Создайте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# 2. Установите зависимости:
pip install -r requirements.txt

# 3. Запустите приложение:
python main.py
# Приложение будет доступно по адресу: http://localhost:5000

# 4. Запуск тестов:
# Все тесты
python -m pytest tests/ -v

# Только API тесты
python -m pytest tests/test_api.py -v

# Только тесты с фабриками
python -m pytest tests/test_factories.py -v

# Конкретный тест
python -m pytest tests/test_api.py::test_exit_without_credit_card -v