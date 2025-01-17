from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskParameters(BaseModel):
    title: str = Field(..., description="The title of the task")
    description: Optional[str] = Field(None, description="Optional description of the task")
    completed: bool = Field(False, description="Whether the task is completed")


class TaskOptionalParameters(BaseModel):
    title: Optional[str] = Field(None, description="The title of the task")
    description: Optional[str] = Field(None, description="Optional description of the task")
    completed: Optional[bool] = Field(None, description="Whether the task is completed")


class TaskInDB(TaskParameters):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
