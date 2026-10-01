from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.note import Note


def search_notes(
    db: Session,
    user_id: UUID,
    query: str,
):
    search_vector = func.to_tsvector(
        "english",
        func.concat(
            Note.title,
            " ",
            Note.body,
        ),
    )

    search_query = func.plainto_tsquery(
        "english",
        query,
    )

    statement = (
        select(Note)
        .where(
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
            search_vector.op("@@")(search_query),
        )
        .order_by(
            func.ts_rank(
                search_vector,
                search_query,
            ).desc()
        )
    )

    return list(db.scalars(statement).all())