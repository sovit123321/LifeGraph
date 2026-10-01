from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.auth.dependencies import get_current_user
from app.core.rate_limit import limiter
from app.db.database import get_db
from app.models.user import User
from app.services.search_service import search_notes_service


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("")
@limiter.limit("30/minute")
def search(
    request: Request,
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return search_notes_service(
        db=db,
        user_id=current_user.id,
        query=q,
    )