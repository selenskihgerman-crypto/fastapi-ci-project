# Скрипт проверки
#!/bin/bash

# Проверка статики
echo "Тест статики:"
curl -I http://localhost/static/test.css

# Проверка API
echo -e "\nТест /hello:"
curl http://localhost/hello

echo -e "\nТест /hello/John:"
curl http://localhost/hello/John

# Проверка тайм-аутов
echo -e "\nЗапуск долгой задачи (5 минут):"
time curl http://localhost/long_task