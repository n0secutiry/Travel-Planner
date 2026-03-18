from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class PlaceBase(BaseModel):
    external_id: int
    title: str


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True


class ProjectPlaceBase(BaseModel):
    notes: Optional[str] = None
    visited: bool = False


class ProjectPlaceCreate(ProjectPlaceBase):
    place_external_id: int


class ProjectPlace(ProjectPlaceBase):
    project_id: int
    place_id: int
    place: Optional[Place] = None

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = []


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    created_at: date
    updated_at: date
    places: List[ProjectPlace] = []

    class Config:
        orm_mode = True
