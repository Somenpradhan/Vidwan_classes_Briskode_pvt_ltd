from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)  # experience, student_reviews, our_students
    student_name = Column(String, nullable=True)
    institute = Column(String, nullable=True)
    course = Column(String, nullable=True)
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
