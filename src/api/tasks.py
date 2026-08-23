from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.task import TaskCreate, TaskResponse
from ..services.task_service import TaskService


router = APIRouter()

service = TaskService()


@router.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db)
):

    tasks = service.get_tasks(db)

    return [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ]


@router.get(
    "/tasks/{id}",
    response_model=TaskResponse
)
def get_task(
    id: int,
    db: Session = Depends(get_db)
):

    task = service.get_task(db, id)

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


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = service.create_task(
        db,
        task_data.title,
        task_data.completed
    )

    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    }


@router.put(
    "/tasks/{id}",
    response_model=TaskResponse
)
def update_task(
    id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = service.update_task(
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


@router.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    id: int,
    db: Session = Depends(get_db)
):

    deleted = service.delete_task(db, id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )

    return