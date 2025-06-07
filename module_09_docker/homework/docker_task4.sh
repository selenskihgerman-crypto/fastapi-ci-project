# 1. Запускаем контейнер (если не запущен):
docker run -d --name test_container python:3.9-slim sleep infinity

# 2. Входим в контейнер и устанавливаем htop:
docker exec -it test_container /bin/bash
apt update && apt install -y htop
htop

# 3. Проверяем путь:
which htop

# Скриншот:
#Терминал с запущенным htop внутри контейнера.
