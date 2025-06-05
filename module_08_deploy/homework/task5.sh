# 1. Реорганизуем структуру:
mkdir -p new_year_application/static
mv new_year_application/css new_year_application/js new_year_application/images new_year_application/static/

# 2. Обновляем ссылки в index.html:
<link rel="stylesheet" href="/static/css/styles.css">
<script src="/static/js/jquery-1.9.1.min.js"></script>

# 3. Модифицируем Flask-приложение:
from flask import send_from_directory

@app.route('/static/<path:filename>')
def send_static(filename):
    return send_from_directory('static', filename)

# 4. Обновляем на сервере:
rsync -avz new_year_application/ newuser@server_ip:/home/newuser/app/
