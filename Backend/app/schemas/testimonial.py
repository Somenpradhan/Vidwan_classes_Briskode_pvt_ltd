from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TestimonialBase(BaseModel):
    student_name: str
    course: Optional[str] = None
    testimonial: str
    photo: Optional[str] = None
    rating: int = 5
    is_featured: bool = True
    is_approved: bool = True


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    student_name: Optional[str] = None
    course: Optional[str] = None
    testimonial: Optional[str] = None
    photo: Optional[str] = None
    rating: Optional[int] = None
    is_featured: Optional[bool] = None
    is_approved: Optional[bool] = None


class TestimonialResponse(TestimonialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
