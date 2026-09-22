from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    slug: str
    title: str
    badge: Optional[str] = None
    target: Optional[str] = None
    category: Optional[str] = "jee"
    image: Optional[str] = None
    tagline: Optional[str] = None
    overview: Optional[str] = None
    duration: Optional[str] = None
    eligibility: Optional[str] = None
    frequency: Optional[str] = None
    highlights: Optional[List[Any]] = []
    curriculum: Optional[List[Any]] = []
    faculties: Optional[List[Any]] = []
    is_active: bool = True
    display_order: int = 0


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    badge: Optional[str] = None
    target: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    tagline: Optional[str] = None
    overview: Optional[str] = None
    duration: Optional[str] = None
    eligibility: Optional[str] = None
    frequency: Optional[str] = None
    highlights: Optional[List[Any]] = None
    curriculum: Optional[List[Any]] = None
    faculties: Optional[List[Any]] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
