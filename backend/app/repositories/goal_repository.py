from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.goal import Goal


def create_goal(
    db: Session,
    user_id: UUID,
    title: str,
    description: str | None,
    status: str,
    priority: str,
    target_date: datetime | None,
):
    goal = Goal(
        user_id=user_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        target_date=target_date,
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


def get_goals(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count(Goal.id)).where(
            Goal.user_id == user_id,
            Goal.deleted_at.is_(None),
        )
    )

    statement = (
        select(Goal)
        .where(
            Goal.user_id == user_id,
            Goal.deleted_at.is_(None),
        )
        .order_by(Goal.created_at.desc())
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

def get_goal(db: Session, user_id: UUID, goal_id: UUID):
    statement = select(Goal).where(
        Goal.id == goal_id,
        Goal.user_id == user_id,
        Goal.deleted_at.is_(None),
    )

    return db.scalars(statement).first()


def update_goal(
    db: Session,
    user_id: UUID,
    goal_id: UUID,
    update_data: dict,
):
    goal = get_goal(db, user_id, goal_id)

    if not goal:
        return None

    for field, value in update_data.items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)

    return goal


def delete_goal(db: Session, user_id: UUID, goal_id: UUID):
    goal = get_goal(db, user_id, goal_id)

    if not goal:
        return None

    goal.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(goal)

    return goal