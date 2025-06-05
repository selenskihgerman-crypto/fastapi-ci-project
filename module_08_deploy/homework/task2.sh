# 1. Создаем папку и файлы конфигурации:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/config
chmod 600 ~/.ssh/config

# 2. Копируем ключи:
cp -fv ~/.ssh/new_user_key* ~/.ssh/
chmod 600 ~/.ssh/new_user_key*

# 3. Редактируем config:
Host server_ip
  User newuser
  IdentityFile ~/.ssh/new_user_key

# 4. Подключаемся:
ssh -v newuser@server_ip
