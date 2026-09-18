from sqlalchemy.orm import Session

from ..models.task import Task


class TaskRepository:

    def create_task(
        self,
        db: Session,
        title: str,
        completed: bool,
        owner_id: int
    ) -> Task:

        task = Task(
            title=title,
            completed=completed,
            owner_id=owner_id
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    def get_tasks(
        self,
        db: Session,
        user_id: int,
        is_admin: bool
    ) -> list[Task]:

        query = db.query(Task)

        if not is_admin:
            query = query.filter(Task.owner_id == user_id)

        return query.all()

    def get_task(
        self,
        db: Session,
        task_id: int
    ) -> Task | None:

        return (
            db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

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