from src.models import Task


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self.next_id = 1

    def add_task(self, title: str) -> Task:
        task = Task(self.next_id, title)
        self.tasks.append(task)
        self.next_id += 1

        return task

    def list_tasks(self) -> list[Task]:
        return self.tasks

    def get_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    def update_task(self, task_id: int, title: str, completed: bool) -> Task | None:

        task = self.get_task(task_id)

        if task is None:
            return None

        task.title = title
        task.completed = completed

        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)

        if task is None:
            return False

        self.tasks.remove(task)
        return True