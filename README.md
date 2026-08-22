# Task Manager API

A REST API version of the Task Manager application built using Python and FastAPI.

The application allows users to create, view, update, and delete tasks through HTTP API endpoints.

Tasks are currently stored in memory using a Python list. The data will be lost when the application is restarted.

---

## Features

- Create a new task
- View all tasks
- View a task by ID
- Update an existing task
- Delete a task
- Request validation using Pydantic
- JSON request and response data
- Appropriate HTTP status codes
- Exception handling for invalid task IDs
- Automatic API documentation using Swagger UI
- Automatic API documentation using ReDoc
- In-memory task storage

---

## Project Structure

Task Manager/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── task_manager.py
│   └── schemas.py
│
├── README.md
├── .gitignore
└── requirements.txt

### File Description

- main.py - FastAPI application and API endpoints
- models.py - Defines the Task class and task properties
- task_manager.py - Contains task management and business logic
- schemas.py - Contains Pydantic models for request validation and response structure
- requirements.txt - Contains Python project dependencies
- README.md - Project documentation
- .gitignore - Specifies files and folders that should not be tracked by Git

---

## Requirements

- Python 3.12 or later
- Git
- FastAPI
- Uvicorn
- Pydantic
- GitHub account for repository hosting

---

## Instructions to Run the Application

### 1. Clone the repository

git clone <repository-url>

### 2. Navigate to the project directory

cd "Task Manager"

### 3. Create a virtual environment

python -m venv .venv

### 4. Activate the virtual environment

#### Windows PowerShell

.venv\Scripts\Activate.ps1

#### Windows Command Prompt

.venv\Scripts\activate.bat

### 5. Install required dependencies

pip install -r requirements.txt

### 6. Run the FastAPI application

From the project root directory, run:

uvicorn src.main:app --reload

The API will start at:

http://127.0.0.1:8000

---

## API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

Open the following URL in a browser:

http://127.0.0.1:8000/docs

Swagger UI allows the API endpoints to be viewed and tested directly from the browser.

### ReDoc

ReDoc documentation is available at:

http://127.0.0.1:8000/redoc

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get a task by ID |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update an existing task |
| DELETE | /tasks/{id} | Delete a task |

---

## API Details

### 1. Get All Tasks

GET /tasks

Returns all tasks currently stored in memory.

Example response:

[
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": false
    },
    {
        "id": 2,
        "title": "Learn REST API",
        "completed": true
    }
]

---

### 2. Get Task by ID

GET /tasks/{id}

Returns a specific task using its ID.

Example:

GET /tasks/1

Response:

{
    "id": 1,
    "title": "Learn FastAPI",
    "completed": false
}

If the task does not exist, the API returns:

404 Not Found

Example response:

{
    "detail": "Task with id 999 not found"
}

---

### 3. Create a Task

POST /tasks

Creates a new task.

Request body:

{
    "title": "Learn FastAPI",
    "completed": false
}

Response:

{
    "id": 1,
    "title": "Learn FastAPI",
    "completed": false
}

Successful task creation returns:

201 Created

---

### 4. Update a Task

PUT /tasks/{id}

Updates an existing task.

Example:

PUT /tasks/1

Request body:

{
    "title": "Learn FastAPI REST API",
    "completed": true
}

Response:

{
    "id": 1,
    "title": "Learn FastAPI REST API",
    "completed": true
}

If the task does not exist:

404 Not Found

---

### 5. Delete a Task

DELETE /tasks/{id}

Deletes a task using its ID.

Example:

DELETE /tasks/1

Successful deletion returns:

204 No Content

If the task does not exist:

404 Not Found

---

## Request Validation

The API uses Pydantic models to validate incoming JSON request data.

For example, the task title must contain at least one character.

Valid request:

{
    "title": "Learn FastAPI",
    "completed": false
}

Invalid request:

{
    "title": "",
    "completed": false
}

The invalid request will be rejected with:

422 Unprocessable Entity

FastAPI also validates the data types.

For example:

{
    "title": "Learn FastAPI",
    "completed": "hello"
}

will result in a validation error because completed must be a Boolean value.

---

## Path Parameter Validation

The task ID is defined as an integer path parameter.

Example:

GET /tasks/1

Here, 1 is the path parameter.

If a non-integer value is provided:

GET /tasks/abc

FastAPI returns:

422 Unprocessable Entity

There is a difference between an invalid ID type and a non-existing task.

For an invalid ID type:

/tasks/abc
    ↓
Invalid integer
    ↓
422 Validation Error

For a non-existing task:

/tasks/999
    ↓
Valid integer but task does not exist
    ↓
404 Not Found

---

## HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request completed successfully |
| 201 | Task created successfully |
| 204 | Task deleted successfully |
| 404 | Task not found |
| 422 | Request validation failed |

---

## Exception Handling

The API uses FastAPI's HTTPException to handle errors.

For example, when a requested task ID does not exist:

GET /tasks/999

The API returns:

404 Not Found

with the response:

{
    "detail": "Task with id 999 not found"
}

This prevents the application from returning incorrect data when an invalid task ID is requested.

---

## Data Storage

The application currently uses in-memory storage.

Tasks are stored in a Python list while the application is running.

Application starts
        ↓
Tasks stored in memory
        ↓
Create / Read / Update / Delete
        ↓
Application stops
        ↓
Data is lost

The application does not use a database yet.

Persistent database storage will be added in the next stage of the project.

---

## Testing

All API endpoints can be tested using the automatically generated Swagger UI.

Open:

http://127.0.0.1:8000/docs

The following operations were tested:

- Create task using POST
- Get all tasks using GET
- Get task by ID using GET
- Update task using PUT
- Delete task using DELETE
- Test invalid task ID
- Test invalid request data
- Test invalid path parameter

---

## Example Workflow

Client
   |
   | HTTP Request
   ↓
FastAPI Application
   |
   ↓
Pydantic Validation
   |
   ↓
Task Manager
   |
   ↓
In-Memory Task List
   |
   ↓
JSON Response
   |
   ↓
Client

---

## Git Branches

This project uses the following branches:

- main
- feature/task-manager

---

## Commit History

Meaningful commits are used to clearly show the development progress.

Example commits include:

- Initialize Task Manager project
- Add task creation functionality
- Add task listing functionality
- Add task completion functionality
- Add task deletion functionality
- Add README with run instructions
- Add gitignore for generated files
- Convert Task Manager into FastAPI REST API

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- Git
- GitHub

---

## Author

Keerthi