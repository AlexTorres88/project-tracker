from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid
from app.db import schemas, update as conn_update, project as conn_project
from app.db.database import get_db

router = APIRouter()

# create update
@router.post("/", response_model=schemas.Update)
def create_update(update: schemas.UpdateCreate, db: Session = Depends(get_db)):
    projects = conn_project.get_project_by_id(db, update.project_id)

    if not projects:
        raise HTTPException(status_code=404, detail="Project id does not exist")

    return conn_update.create_update(db, update)


# delete update
@router.delete("/{id}")
def delete_update(id: uuid.UUID, db: Session = Depends(get_db)):
    conn_update.delete_update(db, id)
    update = conn_update.get_update_by_id(db, id)
    if update:
        raise HTTPException(status_code=500, detail="Error deleting update")

    return {"message": "Successfully deleted update"}
