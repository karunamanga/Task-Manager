from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models.user import User
from ..permissions import user_has_permission
from ..schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskAssign,
    TaskResponse,
)
from ..services.task_service import TaskService


router = APIRouter()
service = TaskService()


@router.get(
    "/tasks",
    response_model=list[TaskResponse],
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not user_has_permission(
        db,
        current_user.id,
        "task",
        "read",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to read tasks",
        )

    can_read_all = user_has_permission(
        db,
        current_user.id,
        "task",
        "read_all",
    )

    return service.get_tasks(
        db,
        current_user.id,
        can_read_all,
    )


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not user_has_permission(
        db,
        current_user.id,
        "task",
        "read",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to read tasks",
        )

    task = service.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    can_read_all = user_has_permission(
        db,
        current_user.id,
        "task",
        "read_all",
    )

    if (
        not can_read_all
        and task.owner_id != current_user.id
        and task.assigned_to_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this task",
        )

    return task


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not user_has_permission(
        db,
        current_user.id,
        "task",
        "create",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create tasks",
        )

    return service.create_task(
        db,
        task_data.title,
        task_data.completed,
        current_user.id,
    )


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not user_has_permission(
        db,
        current_user.id,
        "task",
        "update",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update tasks",
        )

    task = service.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    can_update_all = user_has_permission(
        db,
        current_user.id,
        "task",
        "update_all",
    )

    if (
        not can_update_all
        and task.owner_id != current_user.id
        and task.assigned_to_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this task",
        )

    return service.update_task(
        db,
        task,
        task_data.title,
        task_data.completed,
    )


@router.post(
    "/tasks/{task_id}/assign",
    response_model=TaskResponse,
)
def assign_task(
    task_id: int,
    assignment: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not user_has_permission(
        db,
        current_user.id,
        "task",
        "assign",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to assign tasks",
        )

    task = service.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    assigned_user = (
        db.query(User)
        .filter(User.id == assignment.user_id)
        .first()
    )

    if assigned_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {assignment.user_id} not found",
        )

    return service.assign_task(
        db,
        task,
        assignment.user_id,
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not user_has_permission(
        db,
        current_user.id,
        "task",
        "delete",
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete tasks",
        )

    task = service.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    can_delete_all = user_has_permission(
        db,
        current_user.id,
        "task",
        "delete_all",
    )

    if not can_delete_all and task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this task",
        )

    service.delete_task(db, task_id)

    return None