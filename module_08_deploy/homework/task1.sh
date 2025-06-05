# 1. Создаем новый RSA-ключ на локальной машине:
ssh-keygen -t rsa -b 4096 -f ~/.ssh/new_user_key

# 2. На удаленном сервере создаем пользователя:
adduser newuser

# 3. Копируем публичный ключ на сервер:
ssh-copy-id -i ~/.ssh/new_user_key.pub newuser@server_ip

# 4. Подключаемся с опцией -v:
ssh -v -i ~/.ssh/new_user_key newuser@server_ip

# 5. Удаляем пользователя:
deluser --remove-home newuser
