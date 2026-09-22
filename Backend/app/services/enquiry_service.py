from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryCreate
from app.services.email_service import (
    send_admin_enquiry_notification,
    send_user_enquiry_acknowledgement
)


def create_new_enquiry(
    db: Session,
    enquiry_in: EnquiryCreate,
    background_tasks: BackgroundTasks
) -> Enquiry:
    """
    1. Save enquiry to database.
    2. Queue background email notification to Admin and confirmation to User.
    """
    db_enquiry = Enquiry(
        name=enquiry_in.name,
        email=enquiry_in.email,
        phone=enquiry_in.phone,
        course=enquiry_in.course,
        source=enquiry_in.source or "Website Form",
        message=enquiry_in.message,
        enquiry_type=enquiry_in.enquiry_type or "general",
        status="new"
    )
    db.add(db_enquiry)
    db.commit()
    db.refresh(db_enquiry)

    # Queue background emails
    enquiry_data = {
        "name": db_enquiry.name,
        "email": db_enquiry.email,
        "phone": db_enquiry.phone,
        "course": db_enquiry.course,
        "source": db_enquiry.source,
        "message": db_enquiry.message,
        "enquiry_type": db_enquiry.enquiry_type
    }
    background_tasks.add_task(send_admin_enquiry_notification, enquiry_data)
    
    if db_enquiry.email:
        background_tasks.add_task(
            send_user_enquiry_acknowledgement,
            db_enquiry.email,
            db_enquiry.name
        )

    return db_enquiry
