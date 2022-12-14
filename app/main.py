from fastapi import FastAPI

from app.db import models
from app.db.database import engine

from app.routers import projects, users, updates, points
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(projects.router, prefix="/projects")
app.include_router(users.router, prefix="/users")
app.include_router(updates.router, prefix="/updates")
app.include_router(points.router, prefix="/points")


@app.get("/")
async def root():
    return {"message": settings.postgres_url}
