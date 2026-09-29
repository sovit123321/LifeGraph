from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.auth.jwt import verify_token
from app.db.database import get_db
from app.models.user import User

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = verify_token(token)

        auth_provider_id = payload.get("sub")
        email = payload.get("email")
        name = payload.get("name")

        if not auth_provider_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        user = (
            db.query(User)
            .filter(User.auth_provider_id == auth_provider_id)
            .first()
        )

        if not user:
            user = User(
                auth_provider_id=auth_provider_id,
                email=email,
                name=name,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )