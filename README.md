# Task Manager API

A REST API version of the Task Manager application built using Python and FastAPI.

The application allows users to create, view, update, and delete tasks through HTTP API endpoints.

Tasks are stored persistently in a local PostgreSQL database. Unlike the previous in-memory version, task data is not lost when the FastAPI application is restarted.

The application was later refactored into a clean layered architecture to improve maintainability and separation of responsibilities.

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
- Clean layered backend architecture
- Separation of API, business logic, and database access
- Repository layer for database operations
- Service layer for business logic
- Dependency management using FastAPI dependency injection
- Environment-based database configuration

---

## Project Structure

Task Manager/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── tasks.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── task_repository.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── task.py
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

---

## Layer Responsibilities

The application follows a simple layered architecture:

API → Service → Repository → Database

Each layer has a specific responsibility.

### 1. API / Router Layer

Location:

src/api/tasks.py

The API layer is responsible mainly for HTTP-related concerns.

Responsibilities:

- Define API endpoints
- Receive HTTP requests
- Read path parameters
- Receive request bodies
- Use Pydantic schemas for request validation
- Call the service layer
- Handle HTTP-specific errors
- Return HTTP responses

The API layer should not directly perform database queries.

---

### 2. Service / Business Logic Layer

Location:

src/services/task_service.py

The service layer contains application and business logic.

Responsibilities:

- Coordinate task operations
- Apply business rules when required
- Call the repository layer
- Keep business logic separate from HTTP and database code

The service layer sits between the API and repository.

API → Service → Repository

The current Task Manager application has simple business requirements, so the service layer is intentionally lightweight.

If additional business rules are introduced later, they can be added to the service layer without changing the API or database code.

---

### 3. Repository / Data Access Layer

Location:

src/repositories/task_repository.py

The repository layer is responsible for database access.

Responsibilities:

- Create tasks in the database
- Retrieve all tasks
- Retrieve a task by ID
- Update tasks
- Delete tasks
- Execute SQLAlchemy database operations

The repository contains database-related operations such as:

- db.add()
- db.query()
- db.commit()
- db.refresh()
- db.delete()

The API layer does not directly communicate with PostgreSQL.

---

### 4. Models

Location:

src/models/task.py

Models represent the database structure using SQLAlchemy ORM.

The Task model represents the tasks table in PostgreSQL.

The model contains:

- id
- title
- completed

---

### 5. Schemas / DTOs

Location:

src/schemas/task.py

Schemas define the structure of API request and response data.

The project contains:

TaskCreate

Used for validating incoming task data.

TaskResponse

Used for defining the structure of task responses.

Pydantic performs API-level validation before the request reaches the service layer.

---

### 6. Database Configuration

Location:

src/database.py

The database module is responsible for:

- Loading the database URL
- Creating the SQLAlchemy engine
- Creating database sessions
- Creating the SQLAlchemy Base
- Providing the database session dependency

The PostgreSQL connection string is stored in the .env file.

---

### 7. Dependency Management

FastAPI dependency injection is used to provide a database session to API endpoints.

The get_db() function creates a database session before processing a request and closes the session after the request is completed.

The flow is:

API Request
    ↓
get_db()
    ↓
Database Session
    ↓
API / Service / Repository
    ↓
Database Session Closed

This prevents database sessions from remaining open unnecessarily.

---

## Separation of Concerns

Separation of concerns means dividing the application into different parts where each part has a specific responsibility.

For this application:

API
    ↓
Handles HTTP requests and responses

Service
    ↓
Handles business logic

Repository
    ↓
Handles database operations

Model
    ↓
Represents database tables

Schema
    ↓
Validates API data

Database
    ↓
Manages database connection and sessions

This makes the application easier to understand, maintain, test, and extend.

---

## Single Responsibility

Each major component has one primary responsibility.

Examples:

api/tasks.py

Responsible for HTTP endpoints.

task_service.py

Responsible for application and business logic.

task_repository.py

Responsible for database access.

models/task.py

Responsible for representing the database table.

schemas/task.py

Responsible for request and response data validation.

database.py

Responsible for database connection and session configuration.

This follows the Single Responsibility Principle.

---

## Why Business Logic Should Not Be Placed Directly Inside API Endpoints

API endpoints should mainly handle HTTP-related concerns.

For example:

POST /tasks

The API receives the request and passes the data to the service layer.

It should not directly contain database operations such as:

db.add()
db.commit()
db.query()

Instead, the flow should be:

API
    ↓
Service
    ↓
Repository
    ↓
Database

This keeps the API layer simple and makes the business logic reusable and easier to maintain.

---

## API Validation vs Business Validation

There are two different types of validation.

### API Validation

API validation checks whether the incoming request has the correct structure and data types.

For example:

- title must be a string
- title must contain at least 1 character
- title can contain a maximum of 100 characters
- completed must be a Boolean
- task ID must be an integer

This validation is handled by FastAPI and Pydantic.

Example:

{
    "title": "",
    "completed": false
}

This request fails API validation because the title must contain at least one character.

The API returns:

422 Unprocessable Entity

---

### Business Validation

Business validation checks whether an operation is allowed according to application rules.

For example, if a future requirement says:

"Completed tasks cannot be deleted."

That rule belongs in the service layer.

The service would check the business rule before calling the repository.

Therefore:

API validation
    ↓
Checks request structure and data

Business validation
    ↓
Checks application rules

---

## Configuration Management

The application uses environment variables for configuration.

The PostgreSQL connection string is stored in the .env file.

Example:

DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/task_manager

The application reads the value using python-dotenv.

This prevents database credentials from being hard-coded directly into the source code.

Important:

Do not commit the .env file to Git.

The .gitignore file contains:

.env
.venv/
__pycache__/

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

The PostgreSQL password is stored locally in the .env file and is not included in the repository.

---

## Create the Database

Open PostgreSQL SQL Shell (psql) and connect using the PostgreSQL server details.

Create the database if it does not already exist:

CREATE DATABASE task_manager;

Connect to the database:

\c task_manager

---

## Database Schema

The application uses a tasks table.

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

Create a .env file in the project root directory.

Example:

DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5433/task_manager

Replace YOUR_PASSWORD with the password configured for the local PostgreSQL postgres user.

### Important

Do not commit the .env file to Git because it contains database credentials.

The .gitignore file should contain:

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

Create the task_manager database and tasks table as described in the PostgreSQL Database Setup section.

Create the .env file and configure the DATABASE_URL.

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

API

        ↓

Service

        ↓

Repository

        ↓

SQLAlchemy

        ↓

PostgreSQL

        ↓

tasks Table

        ↓

Data is stored permanently

When the application stops, the data remains in PostgreSQL.

When the application restarts, existing tasks are still available.

Unlike the previous in-memory implementation, restarting the FastAPI application does not remove stored tasks.

---

## Application Architecture

The application follows a layered architecture:

Client

   ↓

API / Router

   ↓

Service / Business Logic

   ↓

Repository / Data Access

   ↓

SQLAlchemy

   ↓

PostgreSQL

---

## Architecture Components

### FastAPI

Handles HTTP requests, API routes, response handling, and automatic API documentation.

### API / Router

Defines endpoints and handles HTTP-specific concerns.

Location:

src/api/tasks.py

### Service

Contains application and business logic and coordinates operations between the API and repository.

Location:

src/services/task_service.py

### Repository

Handles database access and SQLAlchemy operations.

Location:

src/repositories/task_repository.py

### Pydantic Schemas

Validates incoming API data and defines response structures.

Location:

src/schemas/task.py

### SQLAlchemy Model

Represents the PostgreSQL tasks table.

Location:

src/models/task.py

### Database

Manages the PostgreSQL connection, SQLAlchemy engine, sessions, and database dependency.

Location:

src/database.py

### Psycopg

Provides the PostgreSQL database driver used by SQLAlchemy.

### PostgreSQL

Permanently stores task data.

---

## Application Workflow

The request flow is:

Client

   |

   | HTTP Request

   ↓

API / Router

   |

   | Request Validation

   ↓

Service Layer

   |

   | Business Logic

   ↓

Repository Layer

   |

   | Database Operations

   ↓

SQLAlchemy

   |

   ↓

Psycopg

   |

   ↓

PostgreSQL

   |

   ↓

Repository

   |

   ↓

Service

   |

   ↓

API / Router

   |

   | JSON Response

   ↓

Client

---

## Why This Architecture Is Used

The application was refactored to keep different responsibilities separate.

Without separation:

API

   ↓

Database Code

   ↓

Business Logic

All code can become mixed together and difficult to maintain.

With the layered architecture:

API

   ↓

Service

   ↓

Repository

   ↓

Database

Each layer has a clear responsibility.

Benefits include:

- Easier maintenance
- Easier debugging
- Better code organization
- Easier testing
- Easier future changes
- Reduced coupling between layers
- Better separation of concerns

The architecture is intentionally simple and focuses on understanding responsibilities rather than implementing a complex architecture.

---

## Testing

All API endpoints were tested using the automatically generated Swagger UI.

Open:

http://127.0.0.1:8000/docs

The following test cases were successfully completed.

### Test Case 1 - Get All Tasks

Endpoint:

GET /tasks

Result:

200 OK

The API successfully returned the tasks stored in PostgreSQL.

---

### Test Case 2 - Create Task

Endpoint:

POST /tasks

Request:

{
    "title": "Learn Clean Architecture",
    "completed": false
}

Result:

201 Created

A new task was successfully created and stored in PostgreSQL.

---

### Test Case 3 - Get Task by ID

Endpoint:

GET /tasks/{id}

Result:

200 OK

The API successfully returned a specific task using its ID.

---

### Test Case 4 - Update Task

Endpoint:

PUT /tasks/{id}

Request:

{
    "title": "Learn Backend Architecture",
    "completed": true
}

Result:

200 OK

The existing task was successfully updated.

---

### Test Case 5 - Delete Task

Endpoint:

DELETE /tasks/{id}

Result:

204 No Content

The task was successfully deleted.

---

### Test Case 6 - Invalid / Non-existing Task ID

Endpoint:

GET /tasks/999

Result:

404 Not Found

The API correctly returned an error when the requested task did not exist.

Example response:

{
    "detail": "Task with id 999 not found"
}

---

### Test Case 7 - Request Validation

Endpoint:

POST /tasks

Invalid request:

{
    "title": "",
    "completed": false
}

Result:

422 Unprocessable Entity

The API correctly rejected the invalid request because the task title must contain at least one character.

---

## Testing Summary

All 7 test cases passed successfully.

| Test Case | Endpoint | Result |
|---|---|---|
| Get all tasks | GET /tasks | Passed |
| Create task | POST /tasks | Passed |
| Get task by ID | GET /tasks/{id} | Passed |
| Update task | PUT /tasks/{id} | Passed |
| Delete task | DELETE /tasks/{id} | Passed |
| Invalid task ID | GET /tasks/{id} | Passed |
| Request validation | POST /tasks | Passed |

---

## Screenshots

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

An invalid or non-existing task ID was tested and the API returned a 404 Not Found response.

![Invalid Task ID](screenshots/invalid-task-id.png)

### 8. Request Validation

Invalid request data was tested and FastAPI returned a 422 validation error.

![Validation Error](screenshots/validation-error.png)

### 9. PostgreSQL Database

The tasks table was checked using PostgreSQL to verify that task data was stored in the database.

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

## Day 7 Refactoring Summary

The Day 6 Task Manager application was refactored into a clean layered backend structure.

### Before Refactoring

main.py

   ↓

TaskManager

   ↓

PostgreSQL

The API and database operations were more closely coupled.

### After Refactoring

API / Router

   ↓

Service

   ↓

Repository

   ↓

PostgreSQL

The application now separates:

- HTTP concerns
- Business logic
- Database access
- Database models
- API schemas
- Database configuration

### Day 7 Concepts Implemented

- Separation of Concerns
- Single Responsibility
- API / Router Layer
- Service / Business Logic Layer
- Repository / Data Access Layer
- Models
- Schemas / DTOs
- Dependency Management
- API Validation
- Business Validation
- Configuration Management

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
- Refactor Task Manager into layered architecture
- Add repository layer
- Add service layer
- Separate API routes from application entry point
- Organize models and schemas into packages
- Update README for clean architecture

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