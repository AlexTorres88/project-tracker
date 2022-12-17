from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid
from app.db import schemas
from app.db.database import get_db
from app.repositories.points import point as conn_point
from app.repositories.updates import update as conn_update

router = APIRouter()

# create point
@router.post("/", response_model=schemas.Point)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    updates = conn_update.get_update_by_id(db, point.update_id)

    if not updates:
        raise HTTPException(status_code=404, detail="Update id does not exist")

    point = conn_point.create_point(db, point)
    return point


# update point
@router.put("/", response_model=schemas.Point)
def update_point(point: schemas.PointUpdate, db: Session = Depends(get_db)):
    update = conn_point.get_point_by_id(point.id)

    if not update:
        raise HTTPException(status_code=404, detail="Update id does not exist")

    point = conn_point.update_point(db, point)
    return point


# delete point
@router.delete("/{id}")
def delete_point(id: uuid.UUID, db: Session = Depends(get_db)):
    conn_point.delete_point(db, id)
    point = conn_point.get_point_by_id(db, id)
    if point:
        raise HTTPException(status_code=500, detail="Error deleting point")

    return {"message": "Successfully deleted point"}
