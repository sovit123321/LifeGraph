from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.note_tag import NoteTag


def attach_tag_to_note(
    db: Session,
    note_id: UUID,
    tag_id: UUID,
):
    existing = db.scalar(
        select(NoteTag).where(
            NoteTag.note_id == note_id,
            NoteTag.tag_id == tag_id,
        )
    )

    if existing:
        return existing

    note_tag = NoteTag(
        note_id=note_id,
        tag_id=tag_id,
    )

    db.add(note_tag)
    db.commit()
    db.refresh(note_tag)

    return note_tag


def detach_tag_from_note(
    db: Session,
    note_id: UUID,
    tag_id: UUID,
):
    statement = delete(NoteTag).where(
        NoteTag.note_id == note_id,
        NoteTag.tag_id == tag_id,
    )

    result = db.execute(statement)
    db.commit()

    return result.rowcount > 0


def get_note_tags(
    db: Session,
    note_id: UUID,
):
    statement = select(NoteTag).where(
        NoteTag.note_id == note_id
    )

    return list(db.scalars(statement).all())