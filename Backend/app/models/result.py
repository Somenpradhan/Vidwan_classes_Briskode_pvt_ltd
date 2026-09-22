from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    exam = Column(String, nullable=False)  # e.g., JEE Advanced 2024, NEET UG 2024
    rank = Column(String, nullable=False)  # e.g., AIR 42, AIR 115
    year = Column(String, nullable=True)
    college = Column(String, nullable=True)  # e.g., IIT Bombay, AIIMS New Delhi
    course = Column(String, nullable=True)
    achievement = Column(Text, nullable=True)
    photo = Column(String, nullable=True)
    badge_class = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)  # jee, neet, foundation
    is_featured = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
