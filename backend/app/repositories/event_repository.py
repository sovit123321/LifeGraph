from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.event import Event


def create_event(
    db: Session,
    user_id: UUID,
    title: str,
    start_at: datetime,
    end_at: datetime | None,
    all_day: bool,
    task_id: UUID | None,
):
    event = Event(
        user_id=user_id,
        title=title,
        start_at=start_at,
        end_at=end_at,
        all_day=all_day,
        task_id=task_id,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_events(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count(Event.id)).where(
            Event.user_id == user_id,
            Event.deleted_at.is_(None),
        )
    )

    statement = (
        select(Event)
        .where(
            Event.user_id == user_id,
            Event.deleted_at.is_(None),
        )
        .order_by(Event.start_at.asc())
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


def get_event(
    db: Session,
    user_id: UUID,
    event_id: UUID,
):
    statement = select(Event).where(
        Event.id == event_id,
        Event.user_id == user_id,
        Event.deleted_at.is_(None),
    )

    return db.scalars(statement).first()


def update_event(
    db: Session,
    user_id: UUID,
    event_id: UUID,
    title: str | None,
    start_at: datetime | None,
    end_at: datetime | None,
    all_day: bool | None,
    task_id: UUID | None,
):
    event = get_event(db, user_id, event_id)

    if not event:
        return None

    if title is not None:
        event.title = title

    if start_at is not None:
        event.start_at = start_at

    if end_at is not None:
        event.end_at = end_at

    if all_day is not None:
        event.all_day = all_day

    if task_id is not None:
        event.task_id = task_id

    db.commit()
    db.refresh(event)

    return event


def delete_event(
    db: Session,
    user_id: UUID,
    event_id: UUID,
):
    event = get_event(db, user_id, event_id)

    if not event:
        return None

    event.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(event)

    return event