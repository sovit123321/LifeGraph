from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "active"
    github_url: str | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    github_url: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    github_url: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)