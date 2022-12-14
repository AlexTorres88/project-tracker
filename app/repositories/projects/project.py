from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid

from ...db import models, schemas
from app.repositories.users import user as conn_user


def get_projects(
    db: Session, page: int = 1, limit: int = 5, filters: schemas.ProjectFilters = {}
):
    queries = []

    if filters.email:
        user = conn_user.get_user_by_email(db, filters.email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "No projects associated with author",
                    "projects": [],
                },
            )
        queries.append(models.Project.user_id == user.id)
    if filters.title:
        queries.append(models.Project.title == filters.title)
    if filters.status:
        queries.append(models.Project.status == filters.status)

    return (
        db.query(models.Project)
        .filter(*queries)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


def get_project_by_id(db: Session, id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.id == id).first()


def get_projects_by_user(db: Session, user_id: uuid.UUID):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()


def create_project(db: Session, project: schemas.ProjectCreate):

    if project.status not in [e.value for e in schemas.Status]:
        raise HTTPException(status_code=500, detail="Invalid status, use 'pending', 'in_progress' or 'done'")

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
