from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResultBase(BaseModel):
    student_name: str
    exam: str
    rank: str
    year: Optional[str] = None
    college: Optional[str] = None
    course: Optional[str] = None
    achievement: Optional[str] = None
    photo: Optional[str] = None
    badge_class: Optional[str] = "rank-gold"
    category: Optional[str] = "jee"
    is_featured: bool = True
    display_order: int = 0


class ResultCreate(ResultBase):
    pass


class ResultUpdate(BaseModel):
    student_name: Optional[str] = None
    exam: Optional[str] = None
    rank: Optional[str] = None
    year: Optional[str] = None
    college: Optional[str] = None
    course: Optional[str] = None
    achievement: Optional[str] = None
    photo: Optional[str] = None
    badge_class: Optional[str] = None
    category: Optional[str] = None
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None


class ResultResponse(ResultBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
