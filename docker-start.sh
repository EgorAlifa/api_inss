#!/bin/bash

echo "Starting INSS API Service in Docker..."

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
echo "Service is running on http://localhost:9696"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f        # Просмотр логов"
echo "  docker-compose ps             # Статус контейнера"
echo "  docker-compose down           # Остановка сервиса"
echo "  docker-compose restart        # Перезапуск сервиса"
