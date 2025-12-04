#!/bin/bash

echo "Generating self-signed SSL certificate..."

# Создаем директорию для SSL сертификатов
mkdir -p ssl

# Генерируем самоподписанный сертификат
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=INSS/OU=IT/CN=37.252.23.30"

echo "SSL certificate generated successfully!"
echo "Files created:"
echo "  - ssl/cert.pem"
echo "  - ssl/key.pem"
