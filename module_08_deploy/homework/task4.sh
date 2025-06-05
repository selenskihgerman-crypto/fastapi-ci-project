# 1. Добавляем snowstorm.js:
mkdir -p new_year_application/js
wget https://raw.githubusercontent.com/scottschiller/Snowstorm/master/snowstorm.js -O new_year_application/js/snowstorm.js

# 2. Добавляем в index.html:
<script type="text/javascript" src="/js/snowstorm.js"></script>

# 3. Обновляем на сервере:
rsync -avz new_year_application/ newuser@server_ip:/home/newuser/app/
