from uuid import UUID

from sqlalchemy import select, union_all
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.task import Task


def get_timeline(
    db: Session,
    user_id: UUID,
):
    event_query = select(
        Event.id.label("id"),
        Event.title.label("title"),
        Event.start_at.label("timestamp"),
    ).where(
        Event.user_id == user_id,
        Event.deleted_at.is_(None),
    )

    task_query = select(
        Task.id.label("id"),
        Task.title.label("title"),
        Task.created_at.label("timestamp"),
    ).where(
        Task.user_id == user_id,
        Task.deleted_at.is_(None),
    )

    timeline_query = union_all(
        event_query,
        task_query,
    ).order_by(
        "timestamp"
    )

    return db.execute(timeline_query).mappings().all()