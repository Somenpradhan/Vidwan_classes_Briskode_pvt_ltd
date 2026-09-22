from typing import Any
from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.enquiry import EnquiryCreate, EnquiryResponse
from app.services.enquiry_service import create_new_enquiry

router = APIRouter(prefix="/enquiries", tags=["Enquiries"])


@router.post("", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
def submit_general_enquiry(
    enquiry_in: EnquiryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Any:
    """
    Public Endpoint for Hero Inquiry, Apply Now, Callback Request, and Course Inquiry modal forms.
    """
    return create_new_enquiry(db, enquiry_in, background_tasks)
