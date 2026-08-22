from fastapi import FastAPI, HTTPException, status

from src.task_manager import TaskManager
from src.schemas import TaskCreate, TaskResponse


app = FastAPI(
    title="Task Manager API",
    description="REST API for managing tasks",
    version="1.0.0"
)


manager = TaskManager()


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks():
    tasks = manager.list_tasks()

    return [
        {
            "id": task.task_id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ]


@app.get(
    "/tasks/{id}",
    response_model=TaskResponse
)
def get_task(id: int):

    task = manager.get_task(id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    return {
        "id": task.task_id,
        "title": task.title,
        "completed": task.completed
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task_data: TaskCreate):

    task = manager.add_task(task_data.title)

    task.completed = task_data.completed

    return {
        "id": task.task_id,
        "title": task.title,
        "completed": task.completed
    }


@app.put(
    "/tasks/{id}",
    response_model=TaskResponse
)
def update_task(id: int, task_data: TaskCreate):

    task = manager.update_task(
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
        "id": task.task_id,
        "title": task.title,
        "completed": task.completed
    }


@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(id: int):

    deleted = manager.delete_task(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    return