from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.tag_repository import (
    create_tag,
    delete_tag,
    get_tag,
    get_tags,
    update_tag,
)


def create_tag_service(
    db: Session,
    user_id: UUID,
    name: str,
):
    return create_tag(
        db,
        user_id,
        name,
    )


def get_tags_service(
    db: Session,
    user_id: UUID,
):
    return get_tags(
        db,
        user_id,
    )


def get_tag_service(
    db: Session,
    user_id: UUID,
    tag_id: UUID,
):
    return get_tag(
        db,
        user_id,
        tag_id,
    )


def update_tag_service(
    db: Session,
    user_id: UUID,
    tag_id: UUID,
    name: str | None,
):
    return update_tag(
        db,
        user_id,
        tag_id,
        name,
    )


def delete_tag_service(
    db: Session,
    user_id: UUID,
    tag_id: UUID,
):
    return delete_tag(
        db,
        user_id,
        tag_id,
    )