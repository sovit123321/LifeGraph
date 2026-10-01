from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.services.progress_service import get_progress_service


router = APIRouter(
    prefix="/progress",
    tags=["Progress"],
)


@router.get("")
def get_progress_api(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_progress_service(
        db=db,
        user_id=current_user.id,
    )