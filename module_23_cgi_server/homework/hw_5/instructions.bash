#2. Настройка виртуального окружения:
cd ~/PycharmProjects/module_23/wsgi_project
python3 -m venv venv
source venv/bin/activate
pip install gunicorn

#3. Настройка Nginx:
sudo cp config/nginx.conf /etc/nginx/sites-available/wsgi_app
sudo ln -s /etc/nginx/sites-available/wsgi_app /etc/nginx/sites-enabled/
sudo systemctl restart nginx

#4. Запуск Gunicorn:
sudo cp config/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

#5. Проверка:
chmod +x test_script.sh
./test_script.sh