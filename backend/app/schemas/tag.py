from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str | None = None


class TagResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)