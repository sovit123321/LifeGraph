from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event_service import (
    create_event_service,
    delete_event_service,
    get_event_service,
    get_events_service,
    update_event_service,
)


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_event_service(
        db=db,
        user_id=current_user.id,
        title=event_data.title,
        start_at=event_data.start_at,
        end_at=event_data.end_at,
        all_day=event_data.all_day,
        task_id=event_data.task_id,
    )


@router.get("")
def get_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_events_service(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )

@router.get(
    "/{event_id}",
    response_model=EventResponse,
)
def get_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = get_event_service(
        db=db,
        user_id=current_user.id,
        event_id=event_id,
    )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
)
def update_event(
    event_id: UUID,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    update_data = {
        field: getattr(event_data, field)
        for field in event_data.model_fields_set
    }

    event = update_event_service(
        db=db,
        user_id=current_user.id,
        event_id=event_id,
        update_data=update_data,
    )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return event


@router.delete(
    "/{event_id}",
    response_model=EventResponse,
)
def delete_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = delete_event_service(
        db=db,
        user_id=current_user.id,
        event_id=event_id,
    )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return event