from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.tag import Tag
from app.repositories.note_tag_repository import (
    attach_tag_to_note,
    detach_tag_from_note,
    get_note_tags,
)


def verify_note_and_tag(
    db: Session,
    user_id: UUID,
    note_id: UUID,
    tag_id: UUID,
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    tag = (
        db.query(Tag)
        .filter(
            Tag.id == tag_id,
            Tag.user_id == user_id,
        )
        .first()
    )

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return note, tag


def attach_tag_to_note_service(
    db: Session,
    user_id: UUID,
    note_id: UUID,
    tag_id: UUID,
):
    verify_note_and_tag(
        db,
        user_id,
        note_id,
        tag_id,
    )

    return attach_tag_to_note(
        db,
        note_id,
        tag_id,
    )


def detach_tag_from_note_service(
    db: Session,
    user_id: UUID,
    note_id: UUID,
    tag_id: UUID,
):
    verify_note_and_tag(
        db,
        user_id,
        note_id,
        tag_id,
    )

    return detach_tag_from_note(
        db,
        note_id,
        tag_id,
    )


def get_note_tags_service(
    db: Session,
    user_id: UUID,
    note_id: UUID,
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return get_note_tags(
        db,
        note_id,
    )