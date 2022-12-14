from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import user as conn_user, schemas
from app.db.database import get_db

router = APIRouter()

# get users
@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = conn_user.get_users(db)
    return users


# create user
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = conn_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Error registering user")
    return conn_user.create_user(db=db, user=user)
