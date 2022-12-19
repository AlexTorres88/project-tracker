from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from ...db import models, schemas


def get_point_by_id(db: Session, id: uuid.UUID) -> schemas.Point:
    return db.query(models.Point).filter(models.Point.id == id).first()


def get_points_by_update(db: Session, update_id: uuid.UUID):
    return db.query(models.Point).filter(models.Point.update_id == update_id).all()


def create_point(db: Session, point: schemas.PointCreate):
    db_point = models.Point(**point.dict())

    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


def update_point(db: Session, point: schemas.PointUpdate):
    db.query(models.Point).filter(models.Point.id == point.id).update(
        {
            models.Point.description: point.description,
            models.Point.updated_at: datetime.now(),
        },
        synchronize_session=False,
    )
    db.commit()
    return get_point_by_id(db, point.id)


def delete_point(db: Session, id: uuid.UUID):
    db.query(models.Point).filter(models.Point.id == id).delete(
        synchronize_session=False
    )
    db.commit()
