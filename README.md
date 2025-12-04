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

Сервис запустится в фоне на порту **9696** с HTTPS (самоподписанный сертификат).

### 3. Настроить DNS или hosts файл (если нужно)

Если dev.goodt.me еще не указывает на 37.252.23.30, добавьте в файл hosts:

**Windows:** `C:\Windows\System32\drivers\etc\hosts`
**Linux/Mac:** `/etc/hosts`

```
37.252.23.30  dev.goodt.me
```

### 4. Принять самоподписанный SSL сертификат

⚠️ **ВАЖНО:** Первый раз откройте в браузере:
```
https://dev.goodt.me:9696
```

Браузер покажет предупреждение о сертификате. Нажмите:
- Chrome: "Дополнительно" → "Перейти на сайт (небезопасно)"
- Firefox: "Дополнительно" → "Принять риск и продолжить"
- Safari: "Подробнее" → "Посетить этот сайт"

**Примечание:** Сертификат замаскирован под dev.goodt.me с SAN расширением по стандартам Chrome.
После принятия сертификата API будет доступен по HTTPS без блокировки Mixed Content.

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

1. Убедитесь, что сервис запущен
2. **Сначала** откройте `https://dev.goodt.me:9696` в браузере и примите сертификат
3. В виджете API используйте **PUT** или **POST** запрос на `https://dev.goodt.me:9696/api/task`
4. Передайте в теле запроса JSON с `organization_employee` и другими полями
5. Сервис вернет 200 OK с обработанными данными

**Важно:**
- Используйте HTTPS URL с доменом dev.goodt.me
- Сертификат замаскирован под dev.goodt.me с правильными SAN расширениями
- Сначала примите сертификат в браузере, иначе виджет не сможет сделать запрос
