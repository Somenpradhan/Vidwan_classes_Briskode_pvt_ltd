from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    course = Column(String, nullable=True)
    testimonial = Column(Text, nullable=False)
    photo = Column(String, nullable=True)
    rating = Column(Integer, default=5)
    is_featured = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
