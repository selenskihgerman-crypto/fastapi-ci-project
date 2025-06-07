# 1. Логинимся в Docker Hub:
docker login

# 2. Собираем и пушим образ:
docker tag newyear_app ваш_логин/newyear_app:latest
docker push ваш_логин/newyear_app

# 3. На удалённом сервере:
docker pull ваш_логин/newyear_app
docker run -d -p 80:5000 --restart=always ваш_логин/newyear_app

# Ссылка на образ:
#https://hub.docker.com/r/ваш_логин/newyear_app

#Скриншот:
#Работающее приложение на http://IP_сервера.
