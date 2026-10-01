from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GoalCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "active"
    priority: str = "medium"
    target_date: datetime | None = None


class GoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    target_date: datetime | None = None


class GoalResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    priority: str
    target_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)