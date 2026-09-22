from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class EnquiryCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    course: Optional[str] = None
    source: Optional[str] = "Website"
    message: Optional[str] = None
    enquiry_type: Optional[str] = "general"


class EnquiryStatusUpdate(BaseModel):
    status: str  # new, contacted, follow_up, converted, closed


class EnquiryResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: str
    course: Optional[str] = None
    source: Optional[str] = None
    message: Optional[str] = None
    enquiry_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
