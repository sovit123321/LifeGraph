from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.project_repository import (
    create_project,
    delete_project,
    get_project,
    get_projects,
    update_project,
)


def create_project_service(
    db: Session,
    user_id: UUID,
    title: str,
    description: str | None,
    status: str,
    github_url: str | None,
):
    return create_project(
        db,
        user_id,
        title,
        description,
        status,
        github_url,
    )


def get_projects_service(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    return get_projects(
        db=db,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )


def get_project_service(
    db: Session,
    user_id: UUID,
    project_id: UUID,
):
    return get_project(db, user_id, project_id)


def update_project_service(
    db: Session,
    user_id: UUID,
    project_id: UUID,
    title: str | None,
    description: str | None,
    status: str | None,
    github_url: str | None,
):
    return update_project(
        db,
        user_id,
        project_id,
        title,
        description,
        status,
        github_url,
    )


def delete_project_service(
    db: Session,
    user_id: UUID,
    project_id: UUID,
):
    return delete_project(db, user_id, project_id)