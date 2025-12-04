# INSS API Service

Простой API сервис для обработки задач INSS.

## Быстрый старт

### 1. Клонирование или обновление репозитория

```bash
git pull
```

### 2. Запуск сервиса

```bash
./start.sh
```

Сервис запустится на порту **9696**.

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
├── app.py              # Основной файл приложения
├── requirements.txt    # Зависимости Python
├── start.sh           # Скрипт для быстрого запуска
└── README.md          # Документация
```

## Использование с виджетом API в Insight

1. Убедитесь, что сервис запущен на порту 9696
2. В виджете API используйте POST запрос на `http://your-server:9696/api/task`
3. Передайте в теле запроса JSON с `organization_employee` и другими полями
4. Сервис вернет 200 OK с обработанными данными
