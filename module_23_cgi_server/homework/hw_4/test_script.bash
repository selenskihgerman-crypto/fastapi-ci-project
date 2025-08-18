# 4. Скрипт проверки (test_script.sh)
#!/bin/bash

# Проверка статики
echo "Тест статики:"
curl -I http://localhost/static/test.txt

# Проверка API
echo -e "\nТест /hello:"
curl http://localhost/hello

echo -e "\nТест /hello/John:"
curl http://localhost/hello/John

# Проверка 404
echo -e "\nТест неизвестного маршрута:"
curl http://localhost/unknown_route

# Проверка таймаута (запускать вручную при необходимости)
# echo -e "\nТест долгой задачи (5 минут):"
# time curl http://localhost/long_task