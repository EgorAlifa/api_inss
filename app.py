from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import uvicorn
import json
import re

app = FastAPI(title="INSS API Service", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "INSS API Service is running"}


def fix_json_quotes(json_str: str) -> str:
    """
    Исправляет невалидный JSON, добавляя кавычки к незакавыченным значениям
    """
    print(f"[DEBUG] Original JSON: {json_str}")

    # Паттерн для поиска "value": незакавыченное_значение
    # Ловим все между : и следующим } или ,
    pattern = r'"value"\s*:\s*([^"\{\}\[\],][^,\}\]]*?)(?=\s*[,\}\]])'

    def add_quotes(match):
        value = match.group(1).strip()
        print(f"[DEBUG] Found value without quotes: '{value}'")

        # Если значение уже не является числом, null, true, false - добавляем кавычки
        if value not in ['null', 'true', 'false'] and not value.replace('.', '').replace('-', '').isdigit():
            fixed = f'"value": "{value}"'
            print(f"[DEBUG] Fixed to: {fixed}")
            return fixed
        return match.group(0)

    fixed_json = re.sub(pattern, add_quotes, json_str)
    print(f"[DEBUG] Fixed JSON: {fixed_json}")
    return fixed_json


async def parse_request_body(request: Request) -> Any:
    """
    Парсит тело запроса, исправляя невалидный JSON при необходимости
    """
    try:
        # Пытаемся распарсить как обычный JSON
        return await request.json()
    except Exception:
        # Если не получилось, получаем raw body и чиним JSON
        body = await request.body()
        json_str = body.decode('utf-8')

        # Исправляем JSON
        fixed_json = fix_json_quotes(json_str)

        # Парсим исправленный JSON
        return json.loads(fixed_json)


async def process_tasks(data: Any):
    """
    Обрабатывает массив задач и извлекает organization_employee из поля value
    Принимает любые данные без строгой валидации
    """
    try:
        processed_tasks = []

        # Проверяем что data это список
        if not isinstance(data, list):
            data = [data]

        for task in data:
            # Извлекаем organization_employee из fields
            organization_employee = None

            if isinstance(task, dict) and "fields" in task:
                fields = task.get("fields", [])
                if isinstance(fields, list):
                    for field in fields:
                        if isinstance(field, dict):
                            field_type = field.get("type", {})
                            if isinstance(field_type, dict) and field_type.get("id") == 9956:
                                organization_employee = field.get("value")
                                break

            processed_tasks.append({
                "task_id": task.get("id") if isinstance(task, dict) else None,
                "organization_employee": organization_employee,
                "comment": task.get("comment") if isinstance(task, dict) else None,
                "parent": task.get("parent") if isinstance(task, dict) else None
            })

        return {
            "status": "success",
            "message": "Tasks processed successfully",
            "data": processed_tasks
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/task")
async def create_task_post(request: Request):
    """
    POST метод для создания задач - автоматически исправляет невалидный JSON
    """
    data = await parse_request_body(request)
    return await process_tasks(data)


@app.put("/api/task")
async def create_task_put(request: Request):
    """
    PUT метод для создания задач - автоматически исправляет невалидный JSON
    """
    data = await parse_request_body(request)
    return await process_tasks(data)


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
