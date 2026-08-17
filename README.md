# Task Manager

A simple command-line Task Manager built using Python.

## Features

The application supports:

- Add a task
- List tasks
- Mark a task as completed
- Delete a task
- Exit the application

Tasks are stored in memory using a Python list. They will be lost when the application exits.

## Project Structure

```text
task-manager/
│
├── README.md
├── requirements.txt
│
└── src/
    ├── __init__.py
    ├── main.py
    ├── models.py
    └── task_manager.py


    # Task Manager

A simple command-line Task Manager application built using Python. This application allows users to create, view, complete, and delete tasks.

---

## Features

- Add a new task
- View all tasks
- Mark tasks as completed
- Delete tasks
- Simple command-line interface

---

## Project Structure

```text
Task Manager/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── task_manager.py
│
├── README.md
├── .gitignore
└── requirements.txt
```

---

## Requirements

- Python 3.12 or later
- Git

---

## Instructions to Run the Application

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project directory

```bash
cd "Task Manager"
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

### 5. Install required dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python src/main.py
```

---

## Example Usage

```text
1. Add Task
2. View Tasks
3. Mark Task as Completed
4. Delete Task
5. Exit
```

---

## Git Branches

This project uses the following branches:

- `main`
- `feature/task-manager`

---

## Commit History

Meaningful commits are used to clearly show the development progress, such as:

- Initialize Task Manager project
- Add task creation functionality
- Add task listing functionality
- Add task completion functionality
- Add task deletion functionality
- Add README with run instructions
- Add gitignore for generated files

---

## Technologies Used

- Python
- Git
- GitHub

---

## Author

Keerthi