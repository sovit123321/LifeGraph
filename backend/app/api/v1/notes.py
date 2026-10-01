from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import (
    create_note_service,
    delete_note_service,
    get_note_service,
    get_notes_service,
    update_note_service,
)

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_note_service(
        db=db,
        user_id=current_user.id,
        title=note_data.title,
        body=note_data.body,
    )


@router.get("")
def get_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_notes_service(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = get_note_service(
        db=db,
        user_id=current_user.id,
        note_id=note_id,
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note

@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: UUID,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = update_note_service(
        db=db,
        user_id=current_user.id,
        note_id=note_id,
        title=note_data.title,
        body=note_data.body,
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note

@router.delete("/{note_id}", response_model=NoteResponse)
def delete_note(
    note_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = delete_note_service(
        db=db,
        user_id=current_user.id,
        note_id=note_id,
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note