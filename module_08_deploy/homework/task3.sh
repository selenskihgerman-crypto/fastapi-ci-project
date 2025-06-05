# 1. Копируем файлы сайта на сервер:
rsync -avz new_year_application/ newuser@server_ip:/home/newuser/app/

# 2. На сервере устанавливаем зависимости (если нужно):
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask

# 3. Запускаем приложение:
python3 app.py
