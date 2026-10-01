from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.tag_service import (
    create_tag_service,
    delete_tag_service,
    get_tag_service,
    get_tags_service,
    update_tag_service,
)


router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_tag_service(
        db=db,
        user_id=current_user.id,
        name=tag_data.name,
    )


@router.get(
    "",
    response_model=list[TagResponse],
)
def get_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_tags_service(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
)
def get_tag(
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tag = get_tag_service(
        db=db,
        user_id=current_user.id,
        tag_id=tag_id,
    )

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return tag


@router.patch(
    "/{tag_id}",
    response_model=TagResponse,
)
def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tag = update_tag_service(
        db=db,
        user_id=current_user.id,
        tag_id=tag_id,
        name=tag_data.name,
    )

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return tag


@router.delete(
    "/{tag_id}",
    response_model=TagResponse,
)
def delete_tag(
    tag_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tag = delete_tag_service(
        db=db,
        user_id=current_user.id,
        tag_id=tag_id,
    )

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return tag