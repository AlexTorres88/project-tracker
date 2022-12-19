from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

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
    if filters.from_date:
        from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")
        from_date.isoformat(sep="T", timespec="auto")
        queries.append(models.Project.created_at >= from_date)
    if filters.to_date:
        to_date = datetime.strptime(filters.to_date, "%Y-%m-%d")
        to_date.isoformat(sep="T", timespec="auto")
        to_date = to_date.replace(hour=23, minute=59, second=59)
        queries.append(models.Project.created_at <= to_date)

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
        raise HTTPException(
            status_code=500,
            detail="Invalid status, use 'pending', 'in_progress' or 'done'",
        )

    db_project = models.Project(**project.dict())

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project: schemas.ProjectUpdate):

    # create new object to ignore "id" field
    new_proj = {
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "updated_at": datetime.now(),
    }

    update_data = {k: v for k, v in new_proj.items() if v is not None}

    db.query(models.Project).filter(models.Project.id == project.id).update(update_data)

    db.commit()
    return get_project_by_id(db, project.id)


def delete_project(db: Session, id: uuid.UUID):
    db.query(models.Project).filter(models.Project.id == id).delete(
        synchronize_session=False
    )
    db.commit()
