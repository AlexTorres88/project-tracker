from datetime import datetime
from enum import Enum
import uuid

from pydantic import BaseModel


class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class PointBase(BaseModel):
    description: str


class Point(PointBase):
    id: uuid.UUID
    update_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PointCreate(PointBase):
    update_id: uuid.UUID


class UpdateBase(BaseModel):
    title: str


class Update(UpdateBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    points: list[Point] = []

    class Config:
        orm_mode = True


class UpdateCreate(UpdateBase):
    project_id: uuid.UUID


class ProjectBase(BaseModel):
    title: str
    status: str
    description: str


class Project(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: Status
    created_at: datetime
    updated_at: datetime
    updates: list[Update] = []

    class Config:
        orm_mode = True


class ProjectCreate(ProjectBase):
    user_id: uuid.UUID


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    projects: list[Project] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class ProjectFilters(BaseModel):
    email: str = None
    from_date: str = None
    to_date: str = None
    title: str = None
    status: Status = None
