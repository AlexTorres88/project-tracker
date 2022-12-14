from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid
from app.db import project as conn_project, schemas, user as conn_user
from app.db.database import get_db

router = APIRouter()

# get projects
@router.get("/", response_model=list[schemas.Project])
def get(db: Session = Depends(get_db)):
    projects = conn_project.get_projects(db=db)
    return projects


# create project
@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    user = conn_user.get_user(db, project.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid user id")
    return conn_project.create_project(db, project)


# delete project
@router.delete("/{id}")
def delete_project(id: uuid.UUID, db: Session = Depends(get_db)):
    conn_project.delete_project(db, id)
    project = conn_project.get_project_by_id(db, id)
    if project:
        raise HTTPException(status_code=500, detail="Error deleting project")

    return {"message": "Successfully deleted the project"}
