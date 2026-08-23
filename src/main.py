from fastapi import FastAPI

from .api.tasks import router


app = FastAPI(
    title="Task Manager API",
    description="REST API for managing tasks",
    version="1.0.0"
)


app.include_router(router)