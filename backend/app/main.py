import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.core.rate_limit import limiter
from app.api.v1.routes import router
from app.api.v1.notes import router as notes_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.goals import router as goals_router
from app.api.v1.projects import router as projects_router
from app.api.v1.events import router as events_router
from app.api.v1.tags import router as tags_router
from app.api.v1.note_tags import router as note_tags_router
from app.api.v1.documents import router as documents_router
from app.api.v1.search import router as search_router
from app.api.v1.timeline import router as timeline_router
from app.api.v1.progress import router as progress_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("LifeGraph API started")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


app.include_router(router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(goals_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(events_router, prefix="/api/v1")
app.include_router(tags_router, prefix="/api/v1")
app.include_router(note_tags_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(timeline_router, prefix="/api/v1")
app.include_router(progress_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def readiness(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "ready",
        "database": "ok",
    }
