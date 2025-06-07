# 1. Скачиваем образ:
docker pull andreyshulaev1/test_app

# 2. Запускаем контейнер на порту 5050:
docker run -d -p 5050:5050 andreyshulaev1/test_app

# 3. Проверяем работу:
curl http://0.0.0.0:5050/hello/user

# Ожидаемый ответ: Hello, user!

#(Пример)

# text
# CONTAINER ID   IMAGE                     STATUS         PORTS                    NAMES
# a1b2c3d4e5f6   andreyshulaev1/test_app   Up 2 minutes  0.0.0.0:5050->5050/tcp   test_container
