#!/bin/bash

echo "Generating self-signed SSL certificate for dev.goodt.me..."

# Создаем директорию для SSL сертификатов
mkdir -p ssl

# Создаем конфигурационный файл для OpenSSL с SAN (Subject Alternative Name)
cat > ssl/openssl.cnf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext
x509_extensions = v3_ca

[dn]
C=RU
ST=Moscow
L=Moscow
O=GoodT
OU=IT Department
CN=dev.goodt.me

[req_ext]
subjectAltName = @alt_names

[v3_ca]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[alt_names]
DNS.1 = dev.goodt.me
DNS.2 = *.dev.goodt.me
IP.1 = 37.252.23.30
EOF

# Генерируем самоподписанный сертификат с SAN (398 дней - максимум для Chrome)
openssl req -x509 -nodes -days 398 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -config ssl/openssl.cnf

# Удаляем временный конфиг
rm ssl/openssl.cnf

echo ""
echo "✅ SSL certificate generated successfully!"
echo ""
echo "Certificate details:"
echo "  Domain: dev.goodt.me"
echo "  IP: 37.252.23.30"
echo "  Valid for: 398 days"
echo "  Files:"
echo "    - ssl/cert.pem"
echo "    - ssl/key.pem"
