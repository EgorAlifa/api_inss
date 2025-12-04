from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import uvicorn

app = FastAPI(title="INSS API Service", version="1.0.0")


class FieldType(BaseModel):
    id: int


class Field(BaseModel):
    type: FieldType
    value: Any


class TaskRequest(BaseModel):
    parent: Optional[Any] = None
    fields: List[Field]
    comment: str
    id: Any


@app.get("/")
async def root():
    return {"status": "ok", "message": "INSS API Service is running"}


@app.post("/api/task")
async def create_task(tasks: List[TaskRequest]):
    """
    Принимает массив задач и извлекает organization_employee из поля value
    """
    try:
        processed_tasks = []

        for task in tasks:
            # Извлекаем organization_employee из fields
            organization_employee = None
            for field in task.fields:
                if field.type.id == 9956:
                    organization_employee = field.value
                    break

            processed_tasks.append({
                "task_id": task.id,
                "organization_employee": organization_employee,
                "comment": task.comment,
                "parent": task.parent
            })

        return {
            "status": "success",
            "message": "Tasks processed successfully",
            "data": processed_tasks
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
