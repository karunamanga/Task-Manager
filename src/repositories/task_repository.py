from sqlalchemy.orm import Session

from ..models.task import Task


class TaskRepository:

    def create_task(
        self,
        db: Session,
        title: str,
        completed: bool
    ) -> Task:

        task = Task(
            title=title,
            completed=completed
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    def get_tasks(self, db: Session) -> list[Task]:
        return db.query(Task).all()

    def get_task(
        self,
        db: Session,
        task_id: int
    ) -> Task | None:

        return db.query(Task).filter(Task.id == task_id).first()

    def update_task(
        self,
        db: Session,
        task_id: int,
        title: str,
        completed: bool
    ) -> Task | None:

        task = self.get_task(db, task_id)

        if task is None:
            return None

        task.title = title
        task.completed = completed

        db.commit()
        db.refresh(task)

        return task

    def delete_task(
        self,
        db: Session,
        task_id: int
    ) -> bool:

        task = self.get_task(db, task_id)

        if task is None:
            return False

        db.delete(task)
        db.commit()

        return True