from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime | None = None
    all_day: bool = False
    task_id: UUID | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    all_day: bool | None = None
    task_id: UUID | None = None


class EventResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    start_at: datetime
    end_at: datetime | None
    all_day: bool
    task_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)