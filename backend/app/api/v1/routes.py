from fastapi import APIRouter, Depends, Request

from app.core.rate_limit import limiter
from app.core.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter()


@router.get("/test")
def test():
    return {"message": "LifeGraph API is working"}

@router.get("/me", response_model=UserResponse)
@limiter.limit("30/minute")
def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return current_user