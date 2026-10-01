from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.note import Note


def create_note(
    db: Session,
    user_id: UUID,
    title: str,
    body: str,
) -> Note:
    note = Note(
        user_id=user_id,
        title=title,
        body=body,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def get_notes(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count(Note.id)).where(
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
        )
    )

    statement = (
        select(Note)
        .where(
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
        )
        .order_by(Note.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    items = list(db.scalars(statement).all())

    return {
        "items": items,
        "total": total or 0,
        "page": page,
        "page_size": page_size,
    }


def get_note(
    db: Session,
    user_id: UUID,
    note_id: UUID,
) -> Note | None:
    statement = (
        select(Note)
        .where(
            Note.id == note_id,
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
        )
    )

    return db.scalars(statement).first()

def update_note(
    db: Session,
    user_id: UUID,
    note_id: UUID,
    title: str | None,
    body: str | None,
) -> Note | None:
    note = get_note(
        db=db,
        user_id=user_id,
        note_id=note_id,
    )

    if not note:
        return None

    if title is not None:
        note.title = title

    if body is not None:
        note.body = body

    db.commit()
    db.refresh(note)

    return note

def delete_note(
    db: Session,
    user_id: UUID,
    note_id: UUID,
) -> Note | None:
    note = get_note(
        db=db,
        user_id=user_id,
        note_id=note_id,
    )

    if not note:
        return None

    note.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note