from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db import user as conn_user, models, schemas
from app.db.database import SessionLocal, engine

from app.routers import projects
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(projects.router, prefix='/projects')

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = conn_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return conn_user.create_user(db=db, user=user)


@app.get("/")
async def root():
    return { "message": settings.postgres_url }
