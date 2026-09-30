from fastapi import FastAPI
from app.api.v1.routes import router
from app.api.v1.notes import router as notes_router
from app.api.v1.tasks import router as tasks_router

app = FastAPI()


app.include_router(router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}