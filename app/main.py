from fastapi import FastAPI
from app.routers import projects
from app.config import settings

app = FastAPI()

app.include_router(projects.router, prefix='/projects')


@app.get("/")
async def root():
    return { "message": settings.postgres_url }
