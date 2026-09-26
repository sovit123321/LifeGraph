from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test():
    return {"message": "LifeGraph API is working"}