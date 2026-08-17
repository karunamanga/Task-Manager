from models import Task


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, title: str) -> None:
        task_id = len(self.tasks) + 1
        task = Task(task_id, title)
        self.tasks.append(task)

        print("Task added successfully.")

    def list_tasks(self) -> None:
        if not self.tasks:
            print("No tasks available.")
            return

        print("\nTasks:")
        for task in self.tasks:
            task.display()

    def complete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_completed()
                print("Task marked as completed.")
                return

        print("Task not found.")

    def delete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                print("Task deleted successfully.")
                return

        print("Task not found.")