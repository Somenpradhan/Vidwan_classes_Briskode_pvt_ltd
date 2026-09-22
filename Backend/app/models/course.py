from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    badge = Column(String, nullable=True)
    target = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)  # jee, neet, foundation, vst
    image = Column(String, nullable=True)
    tagline = Column(String, nullable=True)
    overview = Column(Text, nullable=True)
    duration = Column(String, nullable=True)
    eligibility = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    
    # Store lists/objects as JSON
    highlights = Column(JSON, nullable=True, default=list)
    curriculum = Column(JSON, nullable=True, default=list)
    faculties = Column(JSON, nullable=True, default=list)

    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
