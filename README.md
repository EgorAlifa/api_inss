# INSS API Service

Простой API сервис для обработки задач INSS.

## Быстрый старт (Docker - рекомендуется)

### 1. Клонирование или обновление репозитория

```bash
git pull
```

### 2. Запуск сервиса в Docker (фоновый режим)

```bash
./docker-start.sh
```

Сервис запустится в фоне на порту **9696** (доступен только локально на 127.0.0.1).

### 3. Настройка HTTPS через nginx (обязательно для работы с dev.goodt.me)

Для работы с HTTPS сайтами нужно добавить location в существующий nginx конфиг:

1. Откройте конфиг nginx для `dev.goodt.me` (обычно в `/etc/nginx/sites-available/`)
2. Добавьте в блок `server` содержимое файла `nginx-location.conf`
3. Проверьте конфигурацию: `sudo nginx -t`
4. Перезагрузите nginx: `sudo systemctl reload nginx`

После этого API будет доступен по адресу: `https://dev.goodt.me/api/inss/api/task`

### Управление Docker контейнером

```bash
# Просмотр логов
docker-compose logs -f

# Статус контейнера
docker-compose ps

# Остановка сервиса
docker-compose down

# Перезапуск сервиса
docker-compose restart
```

## Альтернативный запуск (без Docker)

```bash
./start.sh
```

## API Endpoints

### POST /api/task

Принимает массив задач и обрабатывает их.

**Пример запроса:**

```json
[{
  "parent": null,
  "fields": [
    {
      "type": {
        "id": 9956
      },
      "value": "organization_employee_value"
    }
  ],
  "comment": "string",
  "id": "task_id_123"
}]
```

**Пример ответа:**

```json
{
  "status": "success",
  "message": "Tasks processed successfully",
  "data": [
    {
      "task_id": "task_id_123",
      "organization_employee": "organization_employee_value",
      "comment": "string",
      "parent": null
    }
  ]
}
```

### GET /

Проверка работы сервиса.

**Ответ:**

```json
{
  "status": "ok",
  "message": "INSS API Service is running"
}
```

### GET /health

Health check endpoint.

**Ответ:**

```json
{
  "status": "healthy"
}
```

## Требования

### Для Docker (рекомендуется)
- Docker
- Docker Compose

### Для запуска без Docker
- Python 3.7+
- pip

## Ручная установка

Если не хотите использовать `start.sh`:

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск
python app.py
```

## Структура проекта

```
.
├── app.py                  # Основной файл приложения
├── requirements.txt        # Зависимости Python
├── Dockerfile              # Docker образ
├── docker-compose.yml      # Docker Compose конфигурация
├── docker-start.sh         # Скрипт для запуска в Docker
├── start.sh               # Скрипт для запуска без Docker
├── nginx.conf             # Nginx конфигурация (standalone)
├── nginx-location.conf    # Nginx location для существующего сервера
├── generate-ssl.sh        # Скрипт генерации SSL сертификата
└── README.md              # Документация
```

## Использование с виджетом API в Insight

1. Убедитесь, что сервис запущен и настроен nginx
2. В виджете API используйте **PUT** или **POST** запрос на `https://dev.goodt.me/api/inss/api/task`
3. Передайте в теле запроса JSON с `organization_employee` и другими полями
4. Сервис вернет 200 OK с обработанными данными

**Важно:** Используйте HTTPS, а не HTTP, чтобы избежать блокировки Mixed Content в браузере.
