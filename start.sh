#!/bin/bash

echo "Starting INSS API Service..."

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
echo "Installing dependencies..."
pip install -r requirements.txt

# Запуск сервиса
echo "Starting service on port 9696..."
python app.py
