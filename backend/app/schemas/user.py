from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    auth_provider_id: str
    email: str
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)