from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid
from app.db import schemas, update as conn_update, point as conn_point
from app.db.database import get_db

router = APIRouter()

# create point
@router.post("/", response_model=schemas.Point)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    updates = conn_update.get_update_by_id(db, point.update_id)

    if not updates:
        raise HTTPException(status_code=404, detail="Update id does not exist")

    point = conn_point.create_point(db, point)
    return point


# delete point
@router.delete("/{id}")
def delete_point(id: uuid.UUID, db: Session = Depends(get_db)):
    conn_point.delete_point(db, id)
    point = conn_point.get_point_by_id(db, id)
    if point:
        raise HTTPException(status_code=500, detail="Error deleting point")

    return {"message": "Successfully deleted point"}