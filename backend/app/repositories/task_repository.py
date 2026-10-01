from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.task import Task


def create_task(
    db: Session,
    user_id: UUID,
    title: str,
    description: str | None,
    project_id: UUID | None,
    goal_id: UUID | None,
    status: str,
    due_date: datetime | None,
) -> Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        project_id=project_id,
        goal_id=goal_id,
        status=status,
        due_date=due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_tasks(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.deleted_at.is_(None),
        )
    )

    statement = (
        select(Task)
        .where(
            Task.user_id == user_id,
            Task.deleted_at.is_(None),
        )
        .order_by(Task.created_at.desc())
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


def get_task(
    db: Session,
    user_id: UUID,
    task_id: UUID,
) -> Task | None:
    statement = (
        select(Task)
        .where(
            Task.id == task_id,
            Task.user_id == user_id,
            Task.deleted_at.is_(None),
        )
    )

    return db.scalars(statement).first()


def update_task(
    db: Session,
    user_id: UUID,
    task_id: UUID,
    title: str | None,
    description: str | None,
    project_id: UUID | None,
    goal_id: UUID | None,
    status: str | None,
    due_date: datetime | None,
) -> Task | None:
    task = get_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if not task:
        return None

    if title is not None:
        task.title = title

    if description is not None:
        task.description = description

    if project_id is not None:
        task.project_id = project_id

    if goal_id is not None:
        task.goal_id = goal_id

    if status is not None:
        task.status = status

    if due_date is not None:
        task.due_date = due_date

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    user_id: UUID,
    task_id: UUID,
) -> Task | None:
    task = get_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

    if not task:
        return None

    task.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task