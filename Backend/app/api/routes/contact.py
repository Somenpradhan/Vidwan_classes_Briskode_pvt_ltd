from typing import Any
from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.enquiry import EnquiryCreate, EnquiryResponse
from app.services.enquiry_service import create_new_enquiry

router = APIRouter(tags=["Contact"])


@router.post("/contact", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
def submit_contact_form(
    enquiry_in: EnquiryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Any:
    """
    Public Contact Form Submission.
    Validates form data, saves to PostgreSQL DB, triggers SMTP Admin notification & user receipt email.
    """
    enquiry_in.enquiry_type = "contact"
    enquiry_in.source = enquiry_in.source or "Contact Form Page"
    return create_new_enquiry(db, enquiry_in, background_tasks)
