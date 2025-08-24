# 1. Запустить контейнеры
docker-compose up -d

# 2. Проверить статус контейнеров
docker-compose ps

# 3. Проверить Flask приложение
curl http://localhost:5000/custom

# 4. Сгенерировать тестовые данные
for i in {1..10}; do
  curl http://localhost:5000/custom
  sleep 0.5
done

# 5. Командa для остановки:
docker-compose down