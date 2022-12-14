from sqlalchemy.orm import Session
import uuid
from app.utils import get_password_hash

from ...db import models, schemas


def get_users(db: Session, page: int = 1, limit: int = 5) -> list[schemas.User]:
    return db.query(models.User).offset((page - 1) * limit).limit(limit).all()


def get_user(db: Session, user_id: uuid.UUID) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
