# Запуск:
docker build -t newyear_app .
docker run -d -p 5000:5000 newyear_app

# Браузер с открытым http://0.0.0.0:5000, показывающим количество дней до Нового года.
