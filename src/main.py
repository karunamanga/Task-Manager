from task_manager import TaskManager


def display_menu() -> None:
    print("\n===== Task Manager =====")
    print("1. Add task")
    print("2. List tasks")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Exit")


def main() -> None:
    manager = TaskManager()

    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ").strip()

            if not title:
                print("Task title cannot be empty.")
                continue

            manager.add_task(title)

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID: "))
                manager.complete_task(task_id)
            except ValueError:
                print("Task ID must be a number.")

        elif choice == "4":
            try:
                task_id = int(input("Enter task ID: "))
                manager.delete_task(task_id)
            except ValueError:
                print("Task ID must be a number.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()