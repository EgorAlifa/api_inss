from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import uvicorn

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
    POST метод для создания задач - принимает любой JSON
    """
    data = await request.json()
    return await process_tasks(data)


@app.put("/api/task")
async def create_task_put(request: Request):
    """
    PUT метод для создания задач - принимает любой JSON
    """
    data = await request.json()
    return await process_tasks(data)


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
