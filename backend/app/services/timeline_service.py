from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.timeline_repository import get_timeline


def get_timeline_service(
    db: Session,
    user_id: UUID,
):
    return get_timeline(
        db=db,
        user_id=user_id,
    )