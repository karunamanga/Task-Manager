from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool


class TaskAssign(BaseModel):
    user_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    owner_id: int
    assigned_to_id: int | None = None

    model_config = ConfigDict(from_attributes=True)