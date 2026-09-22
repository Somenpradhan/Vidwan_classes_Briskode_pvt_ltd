from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FacultyBase(BaseModel):
    name: str
    designation: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    specialization: Optional[str] = None
    photo: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    specialization: Optional[str] = None
    photo: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class FacultyResponse(FacultyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
