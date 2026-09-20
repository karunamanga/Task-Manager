from sqlalchemy.orm import Session

from ..models.task import Task
from ..repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self):
        self.repository = TaskRepository()

    def create_task(
        self,
        db: Session,
        title: str,
        completed: bool,
        owner_id: int,
    ) -> Task:
        return self.repository.create_task(
            db,
            title,
            completed,
            owner_id,
        )

    def get_tasks(
        self,
        db: Session,
        user_id: int,
        can_read_all: bool,
    ) -> list[Task]:
        return self.repository.get_tasks(
            db,
            user_id,
            can_read_all,
        )

    def get_task(
        self,
        db: Session,
        task_id: int,
    ) -> Task | None:
        return self.repository.get_task(
            db,
            task_id,
        )

    def update_task(
        self,
        db: Session,
        task: Task,
        title: str,
        completed: bool,
    ) -> Task | None:
        return self.repository.update_task(
            db,
            task,
            title,
            completed,
        )

    def assign_task(
        self,
        db: Session,
        task: Task,
        assigned_to_id: int,
    ) -> Task:
        return self.repository.assign_task(
            db,
            task,
            assigned_to_id,
        )

    def delete_task(
        self,
        db: Session,
        task_id: int,
    ) -> bool:
        return self.repository.delete_task(
            db,
            task_id,
        )