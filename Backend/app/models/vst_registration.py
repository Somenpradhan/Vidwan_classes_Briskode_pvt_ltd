from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base


class VSTRegistration(Base):
    __tablename__ = "vst_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    parent_name = Column(String, nullable=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    class_name = Column(String, nullable=False)
    school = Column(String, nullable=True)
    city = Column(String, nullable=True)
    preferred_center = Column(String, nullable=True)
    exam_type = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String, default="registered", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
