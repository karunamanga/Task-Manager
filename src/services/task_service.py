from sqlalchemy.orm import Session

from ..repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self):
        self.repository = TaskRepository()

    def create_task(
        self,
        db: Session,
        title: str,
        completed: bool
    ):
        return self.repository.create_task(
            db,
            title,
            completed
        )

    def get_tasks(self, db: Session):
        return self.repository.get_tasks(db)

    def get_task(
        self,
        db: Session,
        task_id: int
    ):
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
    ):
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
    ):
        return self.repository.delete_task(
            db,
            task_id
        )