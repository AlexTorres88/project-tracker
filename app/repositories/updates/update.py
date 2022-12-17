from sqlalchemy.orm import Session
import uuid

from ...db import models, schemas


def get_update_by_id(db: Session, id: uuid.UUID):
    return db.query(models.Update).filter(models.Update.id == id).first()


def get_updates_by_project(db: Session, project_id: uuid.UUID):
    return db.query(models.Update).filter(models.Update.project_id == project_id).all()


def create_update(db: Session, update: schemas.UpdateCreate):
    db_update = models.Update(title=update.title, project_id=update.project_id)

    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update


def put_update(db: Session, update: schemas.UpdatePut):
    return (
        db.query(models.Update)
        .filter(models.Update.id == update.id)
        .update({models.Update.title: update.title})
    )


def delete_update(db: Session, id: uuid.UUID):
    db.query(models.Update).filter(models.Update.id == id).delete(
        synchronize_session=False
    )
    db.commit()
