from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task_service,
    delete_task_service,
    get_task_service,
    get_tasks_service,
    update_task_service,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_task_service(
        db=db,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        goal_id=task_data.goal_id,
        status=task_data.status,
        due_date=task_data.due_date,
    )


@router.get("", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_tasks_service(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = get_task_service(
        db=db,
        user_id=current_user.id,
        task_id=task_id,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = update_task_service(
        db=db,
        user_id=current_user.id,
        task_id=task_id,
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        goal_id=task_data.goal_id,
        status=task_data.status,
        due_date=task_data.due_date,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = delete_task_service(
        db=db,
        user_id=current_user.id,
        task_id=task_id,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task