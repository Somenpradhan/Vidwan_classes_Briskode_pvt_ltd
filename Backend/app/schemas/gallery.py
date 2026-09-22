from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class GalleryBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: str
    category: str  # experience, student_reviews, our_students
    student_name: Optional[str] = None
    institute: Optional[str] = None
    course: Optional[str] = None
    display_order: int = 0
    is_featured: bool = True


class GalleryCreate(GalleryBase):
    pass


class GalleryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    student_name: Optional[str] = None
    institute: Optional[str] = None
    course: Optional[str] = None
    display_order: Optional[int] = None
    is_featured: Optional[bool] = None


class GalleryResponse(GalleryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
