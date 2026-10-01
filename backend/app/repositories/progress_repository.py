from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.models.project import Project
from app.models.task import Task


def get_progress(
    db: Session,
    user_id: UUID,
):
    total_tasks = db.scalar(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.deleted_at.is_(None),
        )
    )

    completed_tasks = db.scalar(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.deleted_at.is_(None),
            Task.status == "done",
        )
    )

    total_goals = db.scalar(
        select(func.count(Goal.id)).where(
            Goal.user_id == user_id,
            Goal.deleted_at.is_(None),
        )
    )

    completed_goals = db.scalar(
        select(func.count(Goal.id)).where(
            Goal.user_id == user_id,
            Goal.deleted_at.is_(None),
            Goal.status == "completed",
        )
    )

    active_projects = db.scalar(
        select(func.count(Project.id)).where(
            Project.user_id == user_id,
            Project.deleted_at.is_(None),
            Project.status == "active",
        )
    )

    return {
        "total_tasks": total_tasks or 0,
        "completed_tasks": completed_tasks or 0,
        "pending_tasks": (total_tasks or 0) - (completed_tasks or 0),
        "total_goals": total_goals or 0,
        "completed_goals": completed_goals or 0,
        "active_projects": active_projects or 0,
    }