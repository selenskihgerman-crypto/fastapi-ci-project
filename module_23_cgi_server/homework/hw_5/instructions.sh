# Установка

sudo apt install nginx gunicorn python3-venv
python3 -m venv venv
source venv/bin/activate
pip install gunicorn werkzeug

#------------------------------------------------------------------------

# Запуск

# Nginx
sudo cp nginx_config.conf /etc/nginx/sites-available/wsgi_app
sudo ln -s /etc/nginx/sites-available/wsgi_app /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Gunicorn
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn

#---------------------------------------------------------------------------

# Проверка
chmod +x test_script.sh
./test_script.sh