from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.task_repository import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)


def create_task_service(
    db: Session,
    user_id: UUID,
    title: str,
    description: str | None,
    project_id: UUID | None,
    goal_id: UUID | None,
    status: str,
    due_date: datetime | None,
):
    return create_task(
        db=db,
        user_id=user_id,
        title=title,
        description=description,
        project_id=project_id,
        goal_id=goal_id,
        status=status,
        due_date=due_date,
    )


def get_tasks_service(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    return get_tasks(
        db=db,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )


def get_task_service(
    db: Session,
    user_id: UUID,
    task_id: UUID,
):
    return get_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )


def update_task_service(
    db: Session,
    user_id: UUID,
    task_id: UUID,
    title: str | None,
    description: str | None,
    project_id: UUID | None,
    goal_id: UUID | None,
    status: str | None,
    due_date: datetime | None,
):
    return update_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
        title=title,
        description=description,
        project_id=project_id,
        goal_id=goal_id,
        status=status,
        due_date=due_date,
    )


def delete_task_service(
    db: Session,
    user_id: UUID,
    task_id: UUID,
):
    return delete_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )