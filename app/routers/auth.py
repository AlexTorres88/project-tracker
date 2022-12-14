from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db import schemas
from app.db.database import get_db
from app.repositories.users import user as conn_user
from app.utils import (
    create_access_token,
    verify_password,
)

router = APIRouter()

# register user
@router.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = conn_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Error registering user")
    return conn_user.create_user(db=db, user=user)


# login user
@router.post("/login")
def login_user(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = conn_user.get_user_by_email(db, user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
