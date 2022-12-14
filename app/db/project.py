from sqlalchemy.orm import Session
import uuid

from . import models, schemas

def get_projects_by_user(db: Session, user_id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        **project.dict(),
        user_id=project.user_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project