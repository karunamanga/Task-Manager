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
        owner_id: int
    ) -> Task:

        return self.repository.create_task(
            db,
            title,
            completed,
            owner_id
        )

    def get_tasks(
        self,
        db: Session,
        user_id: int,
        is_admin: bool
    ) -> list[Task]:

        return self.repository.get_tasks(
            db,
            user_id,
            is_admin
        )

    def get_task(
        self,
        db: Session,
        task_id: int
    ) -> Task | None:

        return self.repository.get_task(
            db,
            task_id
        )

    def update_task(
        self,
        db: Session,
        task_id: int,
        title: str,
        completed: bool
    ) -> Task | None:

        return self.repository.update_task(
            db,
            task_id,
            title,
            completed
        )

    def delete_task(
        self,
        db: Session,
        task_id: int
    ) -> bool:

        return self.repository.delete_task(
            db,
            task_id
        )