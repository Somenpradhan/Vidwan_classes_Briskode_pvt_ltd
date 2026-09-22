from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class VSTRegisterRequest(BaseModel):
    student_name: str
    parent_name: Optional[str] = None
    email: EmailStr
    phone: str
    class_name: str
    school: Optional[str] = None
    city: Optional[str] = None
    preferred_center: Optional[str] = None
    exam_type: Optional[str] = None
    message: Optional[str] = None


class VSTRegisterResponse(BaseModel):
    id: int
    student_name: str
    parent_name: Optional[str] = None
    email: str
    phone: str
    class_name: str
    school: Optional[str] = None
    city: Optional[str] = None
    preferred_center: Optional[str] = None
    exam_type: Optional[str] = None
    message: Optional[str] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
