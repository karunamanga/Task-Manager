class Task:
    def __init__(self, task_id: int, title: str):
        self.task_id = task_id
        self.title = title
        self.completed = False

    def mark_completed(self) -> None:
        self.completed = True

    def display(self) -> None:
        status = "Completed" if self.completed else "Pending"
        print(f"{self.task_id}. {self.title} [{status}]")