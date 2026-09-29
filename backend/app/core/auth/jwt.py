from app.core.config import settings

ALGORITHM = "HS256"


def verify_token(token: str) -> dict:
    import jwt

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[ALGORITHM],
    )

    return payload