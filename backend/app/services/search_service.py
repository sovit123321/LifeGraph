from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.search_repository import search_notes


def search_notes_service(
    db: Session,
    user_id: UUID,
    query: str,
):
    return search_notes(
        db,
        user_id,
        query,
    )