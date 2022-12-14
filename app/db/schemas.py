from typing import Union
from datetime import datetime
import uuid

from pydantic import BaseModel

class PointBase(BaseModel):
    description: str

class Point(PointBase):
    id: uuid.UUID
    update_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class PointCreate(PointBase):
    update_id: uuid.UUID

class UpdateBase(BaseModel):
    title: str

class Update(UpdateBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    points = list[Point] = []

class UpdateCreate(UpdateBase):
    project_id: uuid.UUID

class ProjectBase(BaseModel):
    title: str
    status: str
    description: str

class Project(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    updates = list[Update] = []

class ProjectCreate(ProjectBase):
    user_id: uuid.UUID

class UserBase(BaseModel):
    email: str

class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    projects = list[Project] = []

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
