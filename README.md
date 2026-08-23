# Task Manager API

A REST API version of the Task Manager application built using Python and FastAPI.

The application allows users to create, view, update, and delete tasks through HTTP API endpoints.

Tasks are stored persistently in a local PostgreSQL database. Unlike the previous in-memory version, task data is not lost when the FastAPI application is restarted.

---

## Features

- Create a new task
- View all tasks
- View a task by ID
- Update an existing task
- Delete a task
- PostgreSQL persistent database storage
- SQLAlchemy ORM for database operations
- Request validation using Pydantic
- JSON request and response data
- Appropriate HTTP status codes
- Exception handling for invalid task IDs
- Automatic API documentation using Swagger UI
- Automatic API documentation using ReDoc
- Data persistence after application restart

---

## Project Structure

Task Manager/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── task_manager.py
│   ├── schemas.py
│   └── database.py
│
├── screenshots/
│   ├── swagger-ui.png
│   ├── post-task.png
│   ├── get-tasks.png
│   ├── get-task-by-id.png
│   ├── put-task.png
│   ├── delete-task.png
│   ├── invalid-task-id.png
│   ├── validation-error.png
│   ├── database-table.png
│   └── persistence-test.png
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt

### File Description

- main.py - FastAPI application and API endpoints
- database.py - PostgreSQL database connection and SQLAlchemy session configuration
- models.py - SQLAlchemy model representing the database table
- task_manager.py - Contains task CRUD operations and database business logic
- schemas.py - Contains Pydantic models for request validation and response structure
- .env - Stores the PostgreSQL database connection string
- requirements.txt - Contains Python project dependencies
- README.md - Project documentation
- .gitignore - Specifies files and folders that should not be tracked by Git

---

## Requirements

- Python 3.12 or later
- Git
- PostgreSQL
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Psycopg
- python-dotenv
- GitHub account for repository hosting

---

## PostgreSQL Database Setup

The application uses PostgreSQL for persistent task storage.

### Database Configuration

The local PostgreSQL configuration used by the application is:

Host: localhost
Port: 5433
Database: task_manager
Username: postgres

The PostgreSQL password is stored locally in the `.env` file and is not included in the repository.

---

## Create the Database

Open PostgreSQL SQL Shell (psql) and connect using the PostgreSQL server details.

Create the database if it does not already exist:

CREATE DATABASE task_manager;

Connect to the database:

\c task_manager

---

## Database Schema

The application uses a `tasks` table.

Create the table using:

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

### Tasks Table

| Column | Type | Description |
|---|---|---|
| id | SERIAL / Integer | Primary key and automatically generated task ID |
| title | VARCHAR(255) | Task title |
| completed | BOOLEAN | Indicates whether the task is completed |

To verify the table:

\dt

To view the table structure:

\d tasks

To view stored tasks:

SELECT * FROM tasks;

---

## Environment Variables

Create a `.env` file in the project root directory.

Example:

DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/task_manager

Replace `YOUR_PASSWORD` with the password configured for the local PostgreSQL `postgres` user.

### Important

Do not commit the `.env` file to Git because it contains database credentials.

The `.gitignore` file should contain:

.env
.venv/
__pycache__/

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

### 6. Configure PostgreSQL

Make sure the local PostgreSQL server is running.

Create the `task_manager` database and `tasks` table as described in the PostgreSQL Database Setup section.

Create the `.env` file and configure the `DATABASE_URL`.

### 7. Run the FastAPI application

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

ReDoc provides an alternative documentation interface for the API.

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

Returns all tasks stored in the PostgreSQL database.

Example response:

[
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": false
    },
    {
        "id": 2,
        "title": "Learn PostgreSQL",
        "completed": true
    }
]

Successful request returns:

200 OK

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

Successful request returns:

200 OK

If the task does not exist:

404 Not Found

Example response:

{
    "detail": "Task with id 999 not found"
}

---

### 3. Create a Task

POST /tasks

Creates a new task and stores it in the PostgreSQL database.

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

The task ID is automatically generated by PostgreSQL.

---

### 4. Update a Task

PUT /tasks/{id}

Updates an existing task in the PostgreSQL database.

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

Successful update returns:

200 OK

If the task does not exist:

404 Not Found

---

### 5. Delete a Task

DELETE /tasks/{id}

Deletes a task from the PostgreSQL database.

Example:

DELETE /tasks/1

Successful deletion returns:

204 No Content

If the task does not exist:

404 Not Found

---

## Request Validation

The API uses Pydantic models to validate incoming JSON request data.

The task title must contain at least one character and can contain a maximum of 100 characters.

### Valid Request

{
    "title": "Learn FastAPI",
    "completed": false
}

### Invalid Request

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

For example:

GET /tasks/999

If task 999 does not exist, the API returns:

404 Not Found

with the response:

{
    "detail": "Task with id 999 not found"
}

This prevents the application from returning incorrect data when an invalid task ID is requested.

---

## Database Storage

The application uses PostgreSQL for persistent data storage.

Tasks are no longer stored in a Python list.

The data flow is:

Application starts

        ↓

FastAPI connects to PostgreSQL

        ↓

Create / Read / Update / Delete

        ↓

Tasks stored in PostgreSQL

        ↓

Application stops

        ↓

Data remains in PostgreSQL

        ↓

Application restarts

        ↓

Existing tasks are still available

Unlike the previous in-memory implementation, restarting the FastAPI application does not remove stored tasks.

---

## Database Architecture

The application uses SQLAlchemy as the ORM for interacting with PostgreSQL.

FastAPI

   ↓

Pydantic Validation

   ↓

Database Session

   ↓

Task Manager

   ↓

SQLAlchemy Model

   ↓

Psycopg Driver

   ↓

PostgreSQL

   ↓

task_manager Database

   ↓

tasks Table

### Components

FastAPI

Handles HTTP requests and API routes.

Pydantic

Validates request and response data.

TaskManager

Contains the CRUD business logic.

SQLAlchemy

Maps the Python Task model to the PostgreSQL tasks table and performs database operations.

Psycopg

Provides the PostgreSQL database driver used by SQLAlchemy.

PostgreSQL

Permanently stores the task data.

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

Database Session

   |

   ↓

Task Manager

   |

   ↓

SQLAlchemy

   |

   ↓

PostgreSQL

   |

   ↓

tasks Table

   |

   ↓

JSON Response

   |

   ↓

Client

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
- Verify tasks are stored in PostgreSQL
- Restart the FastAPI application and verify that existing tasks remain

### 1. Swagger UI - API Documentation

Swagger UI displays all available API endpoints and allows them to be tested directly from the browser.

![Swagger UI](screenshots/swagger-ui.png)

### 2. Create Task - POST /tasks

A new task was successfully created using the POST endpoint and stored in PostgreSQL.

![POST Create Task](screenshots/post-task.png)

### 3. Get All Tasks - GET /tasks

The GET endpoint successfully returned all tasks stored in PostgreSQL.

![GET All Tasks](screenshots/get-tasks.png)

### 4. Get Task by ID - GET /tasks/{id}

The API successfully returned a specific task using its ID.

![GET Task by ID](screenshots/get-task-by-id.png)

### 5. Update Task - PUT /tasks/{id}

The existing task was successfully updated in PostgreSQL using the PUT endpoint.

![PUT Update Task](screenshots/put-task.png)

### 6. Delete Task - DELETE /tasks/{id}

The task was successfully deleted from PostgreSQL using the DELETE endpoint.

![DELETE Task](screenshots/delete-task.png)

### 7. Invalid Task ID

An invalid task ID was tested and the API returned a 404 Not Found response.

![Invalid Task ID](screenshots/invalid-task-id.png)

### 8. Request Validation

Invalid request data was tested and FastAPI returned a 422 validation error.

![Validation Error](screenshots/validation-error.png)

### 9. PostgreSQL Database

The `tasks` table was checked using PostgreSQL to verify that task data was stored in the database.

![PostgreSQL Database](screenshots/database-table.png)

### 10. Data Persistence After Restart

The FastAPI application was stopped and restarted. Previously created tasks were still available after the restart, confirming that PostgreSQL provides persistent storage.

![Persistence Test](screenshots/persistence-test.png)

---

## Data Persistence Verification

To verify that data is not lost after restarting the application:

### Step 1

Create a task using:

POST /tasks

### Step 2

Verify that the task exists:

GET /tasks

### Step 3

Stop the FastAPI application:

Ctrl + C

### Step 4

Restart the application:

uvicorn src.main:app --reload

### Step 5

Call:

GET /tasks

The previously created task should still be returned.

This confirms that the application uses persistent PostgreSQL storage instead of temporary in-memory storage.

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
- Add PostgreSQL database connection
- Add SQLAlchemy task model
- Replace in-memory storage with PostgreSQL
- Add PostgreSQL CRUD operations
- Update README for PostgreSQL persistence

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Psycopg
- PostgreSQL
- python-dotenv
- Git
- GitHub

---

## Author

Keerthi