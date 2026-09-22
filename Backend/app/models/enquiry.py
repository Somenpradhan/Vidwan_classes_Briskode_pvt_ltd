from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    course = Column(String, nullable=True)
    source = Column(String, nullable=True)  # e.g., "Homepage Hero Form", "Contact Page"
    message = Column(Text, nullable=True)
    enquiry_type = Column(String, nullable=False, default="general", index=True) 
    # hero_inquiry, contact, application, callback, demo, course_enquiry, vst, other
    
    status = Column(String, default="new", index=True) 
    # new, contacted, follow_up, converted, closed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
