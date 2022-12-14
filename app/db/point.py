from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def get_points_by_update(db: Session, update_id: uuid.UUID):
    return db.query(models.Point).filter(models.Point.update_id == update_id).all()

def create_point(db: Session, point: schemas.PointCreate):
    db_point = models.Point(title=point.title, update_id=point.update_id)

    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point