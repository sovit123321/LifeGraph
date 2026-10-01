from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.services.goal_service import (
    create_goal_service,
    delete_goal_service,
    get_goal_service,
    get_goals_service,
    update_goal_service,
)


router = APIRouter(
    prefix="/goals",
    tags=["Goals"],
)


@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_goal_service(
        db=db,
        user_id=current_user.id,
        title=goal_data.title,
        description=goal_data.description,
        status=goal_data.status,
        priority=goal_data.priority,
        target_date=goal_data.target_date,
    )


@router.get("")
def get_goals(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_goals_service(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )

@router.get(
    "/{goal_id}",
    response_model=GoalResponse,
)
def get_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = get_goal_service(
        db=db,
        user_id=current_user.id,
        goal_id=goal_id,
    )

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return goal


@router.patch(
    "/{goal_id}",
    response_model=GoalResponse,
)
def update_goal(
    goal_id: UUID,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = update_goal_service(
        db=db,
        user_id=current_user.id,
        goal_id=goal_id,
        title=goal_data.title,
        description=goal_data.description,
        status=goal_data.status,
        priority=goal_data.priority,
        target_date=goal_data.target_date,
    )

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return goal


@router.delete(
    "/{goal_id}",
    response_model=GoalResponse,
)
def delete_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = delete_goal_service(
        db=db,
        user_id=current_user.id,
        goal_id=goal_id,
    )

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return goal