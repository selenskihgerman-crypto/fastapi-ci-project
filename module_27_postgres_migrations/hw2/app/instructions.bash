# Инструкция по запуску и проверке приложения

## Предварительные требования:
- PostgreSQL установлен и запущен
- Python 3.8+ установлен


## 1. Настройка базы данных:
```bash
# Создать пользователя и базу
sudo -u postgres psql -c "CREATE USER skillbox_user WITH PASSWORD 'password';"
sudo -u postgres psql -c "CREATE DATABASE skillbox_db OWNER skillbox_user;"


# 2. Установка зависимостей:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# 3. Создание таблиц:
python -c "
from app import Base, engine
Base.metadata.create_all(bind=engine)
print('Таблицы созданы!')
"


# 4. Запуск приложения:
python app.py


# 5. Проверка endpoints (в новом терминале):

    # 1. Главная страница:
    curl http://localhost:5000/


    # 2. Добавление пользователя (запустит инициализацию данных):
    curl -X POST http://localhost:5000/add_user \
   -H "Content-Type: application/json" \
   -d '{"name":"Тестовый Пользователь"}'


    # 3. Поиск кофе:
    curl "http://localhost:5000/search_coffee?q=coffee"


# 6. Проверка данных в базе:
PGPASSWORD=password psql -U skillbox_user -d skillbox_db -h localhost -c "\dt"
PGPASSWORD=password psql -U skillbox_user -d skillbox_db -h localhost -c "SELECT * FROM coffee;"
PGPASSWORD=password psql -U skillbox_user -d skillbox_db -h localhost -c "SELECT * FROM users;"


# 7. Проверка миграций Alembic:
# История миграций
alembic history

# Текущая версия
alembic current

# Применить миграции
alembic upgrade head

