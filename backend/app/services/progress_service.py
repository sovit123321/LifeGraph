from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.progress_repository import get_progress


def get_progress_service(
    db: Session,
    user_id: UUID,
):
    return get_progress(
        db=db,
        user_id=user_id,
    )