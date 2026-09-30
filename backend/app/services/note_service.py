from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.note_repository import (
    create_note,
    delete_note,
    get_note,
    get_notes,
    update_note,
)

def create_note_service(
    db: Session,
    user_id: UUID,
    title: str,
    body: str,
):
    return create_note(
        db=db,
        user_id=user_id,
        title=title,
        body=body,
    )


def get_notes_service(
    db: Session,
    user_id: UUID,
):
    return get_notes(
        db=db,
        user_id=user_id,
    )


def get_note_service(
    db: Session,
    user_id: UUID,
    note_id: UUID,
):
    return get_note(
        db=db,
        user_id=user_id,
        note_id=note_id,
    )


def update_note_service(
    db: Session,
    user_id: UUID,
    note_id: UUID,
    title: str | None,
    body: str | None,
):
    return update_note(
        db=db,
        user_id=user_id,
        note_id=note_id,
        title=title,
        body=body,
    )

def delete_note_service(
    db: Session,
    user_id: UUID,
    note_id: UUID,
):
    return delete_note(
        db=db,
        user_id=user_id,
        note_id=note_id,
    )

