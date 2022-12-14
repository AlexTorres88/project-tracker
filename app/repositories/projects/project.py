from sqlalchemy.orm import Session
import uuid

from ...db import models, schemas


def get_projects(db: Session):
    return db.query(models.Project).all()


def get_project_by_id(db: Session, id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.id == id).first()


def get_projects_by_user(db: Session, user_id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, id: uuid.UUID):
    db.query(models.Project).filter(models.Project.id == id).delete(
        synchronize_session=False
    )
    db.commit()
