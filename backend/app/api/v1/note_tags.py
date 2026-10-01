from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.services.note_tag_service import (
    attach_tag_to_note_service,
    detach_tag_from_note_service,
    get_note_tags_service,
)


router = APIRouter(
    prefix="/notes",
    tags=["Note Tags"],
)


@router.post(
    "/{note_id}/tags/{tag_id}",
    status_code=status.HTTP_201_CREATED,
)
def attach_tag(
    note_id: UUID,
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attach_tag_to_note_service(
        db=db,
        user_id=current_user.id,
        note_id=note_id,
        tag_id=tag_id,
    )

    return {
        "message": "Tag attached to note successfully"
    }


@router.delete(
    "/{note_id}/tags/{tag_id}",
)
def detach_tag(
    note_id: UUID,
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    detached = detach_tag_from_note_service(
        db=db,
        user_id=current_user.id,
        note_id=note_id,
        tag_id=tag_id,
    )

    if not detached:
        return {
            "message": "Tag was not attached to this note"
        }

    return {
        "message": "Tag detached from note successfully"
    }


@router.get(
    "/{note_id}/tags",
)
def get_note_tags(
    note_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_note_tags_service(
        db=db,
        user_id=current_user.id,
        note_id=note_id,
    )