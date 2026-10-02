from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.project import Project


def create_project(
    db: Session,
    user_id: UUID,
    title: str,
    description: str | None,
    status: str,
    github_url: str | None,
):
    project = Project(
        user_id=user_id,
        title=title,
        description=description,
        status=status,
        github_url=github_url,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_project(
    db: Session,
    user_id: UUID,
    project_id: UUID,
):
    statement = select(Project).where(
        Project.id == project_id,
        Project.user_id == user_id,
        Project.deleted_at.is_(None),
    )

    return db.scalars(statement).first()

def get_projects(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count(Project.id)).where(
            Project.user_id == user_id,
            Project.deleted_at.is_(None),
        )
    )

    statement = (
        select(Project)
        .where(
            Project.user_id == user_id,
            Project.deleted_at.is_(None),
        )
        .order_by(Project.created_at.desc())
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


def update_project(
    db: Session,
    user_id: UUID,
    project_id: UUID,
    update_data: dict,
):
    project = get_project(db, user_id, project_id)

    if not project:
        return None

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(db: Session, user_id: UUID, project_id: UUID):
    project = get_project(db, user_id, project_id)

    if not project:
        return None

    project.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(project)

    return project