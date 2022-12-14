from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import schemas
from app.db.database import get_db
from app.repositories.users import user as conn_user

router = APIRouter()

# get users
@router.get("/", response_model=list[schemas.User])
def get_users(page: int = 1, limit: int = 5, db: Session = Depends(get_db)):
    users = conn_user.get_users(db, page, limit)
    print(users)
    return users
