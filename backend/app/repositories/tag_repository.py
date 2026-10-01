from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag


def create_tag(
    db: Session,
    user_id: UUID,
    name: str,
):
    tag = Tag(
        user_id=user_id,
        name=name,
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def get_tags(
    db: Session,
    user_id: UUID,
):
    statement = (
        select(Tag)
        .where(Tag.user_id == user_id)
        .order_by(Tag.name.asc())
    )

    return list(db.scalars(statement).all())


def get_tag(
    db: Session,
    user_id: UUID,
    tag_id: UUID,
):
    statement = select(Tag).where(
        Tag.id == tag_id,
        Tag.user_id == user_id,
    )

    return db.scalars(statement).first()


def update_tag(
    db: Session,
    user_id: UUID,
    tag_id: UUID,
    name: str | None,
):
    tag = get_tag(db, user_id, tag_id)

    if not tag:
        return None

    if name is not None:
        tag.name = name

    db.commit()
    db.refresh(tag)

    return tag


def delete_tag(
    db: Session,
    user_id: UUID,
    tag_id: UUID,
):
    tag = get_tag(db, user_id, tag_id)

    if not tag:
        return None

    db.delete(tag)
    db.commit()

    return tag