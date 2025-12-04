#!/bin/bash

echo "Starting INSS API Service in Docker with HTTPS..."

# Генерация SSL сертификата если не существует
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    echo "Generating self-signed SSL certificate..."
    ./generate-ssl.sh
fi

# Остановка и удаление старого контейнера если он существует
docker-compose down

# Сборка и запуск в фоне
docker-compose up -d --build

# Проверка статуса
echo ""
echo "Checking service status..."
sleep 3
docker-compose ps

echo ""
echo "Service is running on https://37.252.23.30:9696"
echo ""
echo "⚠️  ВАЖНО: Первый раз откройте https://37.252.23.30:9696 в браузере"
echo "    и примите самоподписанный сертификат (нажмите 'Продолжить')"
echo ""
echo "API теперь принимает любые данные без строгой валидации!"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f        # Просмотр логов"
echo "  docker-compose ps             # Статус контейнера"
echo "  docker-compose down           # Остановка сервиса"
echo "  docker-compose restart        # Перезапуск сервиса"
