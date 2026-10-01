from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.goal_repository import (
    create_goal,
    delete_goal,
    get_goal,
    get_goals,
    update_goal,
)


def create_goal_service(
    db: Session,
    user_id: UUID,
    title: str,
    description: str | None,
    status: str,
    priority: str,
    target_date: datetime | None,
):
    return create_goal(
        db,
        user_id,
        title,
        description,
        status,
        priority,
        target_date,
    )


def get_goals_service(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    return get_goals(
        db=db,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )


def get_goal_service(db: Session, user_id: UUID, goal_id: UUID):
    return get_goal(db, user_id, goal_id)


def update_goal_service(
    db: Session,
    user_id: UUID,
    goal_id: UUID,
    title: str | None,
    description: str | None,
    status: str | None,
    priority: str | None,
    target_date: datetime | None,
):
    return update_goal(
        db,
        user_id,
        goal_id,
        title,
        description,
        status,
        priority,
        target_date,
    )


def delete_goal_service(
    db: Session,
    user_id: UUID,
    goal_id: UUID,
):
    return delete_goal(db, user_id, goal_id)