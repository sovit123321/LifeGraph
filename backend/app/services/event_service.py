from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.event_repository import (
    create_event,
    delete_event,
    get_event,
    get_events,
    update_event,
)


def create_event_service(
    db: Session,
    user_id: UUID,
    title: str,
    start_at: datetime,
    end_at: datetime | None,
    all_day: bool,
    task_id: UUID | None,
):
    return create_event(
        db,
        user_id,
        title,
        start_at,
        end_at,
        all_day,
        task_id,
    )


def get_events_service(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    return get_events(
        db=db,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )


def get_event_service(
    db: Session,
    user_id: UUID,
    event_id: UUID,
):
    return get_event(db, user_id, event_id)


def update_event_service(
    db: Session,
    user_id: UUID,
    event_id: UUID,
    title: str | None,
    start_at: datetime | None,
    end_at: datetime | None,
    all_day: bool | None,
    task_id: UUID | None,
):
    return update_event(
        db,
        user_id,
        event_id,
        title,
        start_at,
        end_at,
        all_day,
        task_id,
    )


def delete_event_service(
    db: Session,
    user_id: UUID,
    event_id: UUID,
):
    return delete_event(db, user_id, event_id)