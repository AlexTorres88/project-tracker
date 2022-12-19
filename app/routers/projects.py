from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import uuid
from app.db import schemas
from app.db.database import get_db
from app.repositories.projects import project as conn_project
from app.repositories.users import user as conn_user

router = APIRouter()

# get projects
@router.get("/", response_model=list[schemas.Project])
def get(
    page: int = 1,
    limit: int = Query(5, description="Limit per page"),
    author: str = Query(None, description="Has to exactly match the author's email"),
    title: str = Query(None, description="Has to exactly match the project's title"),
    status: schemas.Status = None,
    from_date: str = Query(
        None,
        regex="(\d{4})[/.-](\d{2})[/.-](\d{2})$",
        description="Projects from or after this date, format YYYY-MM-DD",
    ),
    to_date: str = Query(
        None,
        regex="(\d{4})[/.-](\d{2})[/.-](\d{2})$",
        description="Projects in or before this date, format YYYY-MM-DD",
    ),
    db: Session = Depends(get_db),
):
    filters = schemas.ProjectFilters(
        email=author, title=title, status=status, from_date=from_date, to_date=to_date
    )
    projects = conn_project.get_projects(db, page, limit, filters)
    return projects


# create project
@router.post("/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    user = conn_user.get_user(db, project.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid user id")
    return conn_project.create_project(db, project)


# update project
@router.put("/", response_model=schemas.Project)
def update_project(project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project_exist = conn_project.get_project_by_id(db, project.id)

    if not project_exist:
        raise HTTPException(status_code=404, detail="Project id does not exist")

    return conn_project.update_project(db, project)


# delete project
@router.delete("/{id}")
def delete_project(id: uuid.UUID, db: Session = Depends(get_db)):
    conn_project.delete_project(db, id)
    project = conn_project.get_project_by_id(db, id)
    if project:
        raise HTTPException(status_code=500, detail="Error deleting project")

    return {"message": "Successfully deleted the project"}
