from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.schemas import TaskCreate, TaskResponse
from src.task_manager import TaskManager


app = FastAPI(
    title="Task Manager API",
    description="REST API for managing tasks",
    version="1.0.0"
)


manager = TaskManager()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(db: Session = Depends(get_db)):

    tasks = manager.list_tasks(db)

    return [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ]


@app.get(
    "/tasks/{id}",
    response_model=TaskResponse
)
def get_task(
    id: int,
    db: Session = Depends(get_db)
):

    task = manager.get_task(db, id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = manager.add_task(
        db,
        task_data.title,
        task_data.completed
    )

    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    }


@app.put(
    "/tasks/{id}",
    response_model=TaskResponse
)
def update_task(
    id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = manager.update_task(
        db,
        id,
        task_data.title,
        task_data.completed
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    }


@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    id: int,
    db: Session = Depends(get_db)
):

    deleted = manager.delete_task(db, id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    return