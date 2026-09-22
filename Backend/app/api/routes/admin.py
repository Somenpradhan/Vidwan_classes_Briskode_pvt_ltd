from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.enquiry import Enquiry
from app.models.vst_registration import VSTRegistration
from app.models.newsletter import NewsletterSubscriber
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.result import Result
from app.models.gallery import GalleryItem
from app.models.testimonial import Testimonial
from app.models.user import User
from app.schemas.enquiry import EnquiryResponse, EnquiryStatusUpdate
from app.schemas.vst import VSTRegisterResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Get aggregated counts for admin dashboard analytics.
    """
    total_enquiries = db.query(Enquiry).count()
    new_enquiries = db.query(Enquiry).filter(Enquiry.status == "new").count()
    contacted_enquiries = db.query(Enquiry).filter(Enquiry.status == "contacted").count()
    applications = db.query(Enquiry).filter(Enquiry.enquiry_type == "application").count()
    vst_registrations = db.query(VSTRegistration).count()
    newsletter_subscribers = db.query(NewsletterSubscriber).count()
    courses_count = db.query(Course).count()
    faculty_count = db.query(Faculty).count()
    results_count = db.query(Result).count()
    gallery_images = db.query(GalleryItem).count()
    testimonials_count = db.query(Testimonial).count()

    return {
        "total_enquiries": total_enquiries,
        "new_enquiries": new_enquiries,
        "contacted_enquiries": contacted_enquiries,
        "applications": applications,
        "vst_registrations": vst_registrations,
        "newsletter_subscribers": newsletter_subscribers,
        "courses": courses_count,
        "faculty": faculty_count,
        "results": results_count,
        "gallery_images": gallery_images,
        "testimonials": testimonials_count
    }


@router.get("/enquiries", response_model=List[EnquiryResponse])
def list_enquiries(
    status_filter: Optional[str] = None,
    enquiry_type: Optional[str] = None,
    course: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    List all enquiries with filtering & pagination (Admin only).
    """
    query = db.query(Enquiry)
    if status_filter:
        query = query.filter(Enquiry.status == status_filter)
    if enquiry_type:
        query = query.filter(Enquiry.enquiry_type == enquiry_type)
    if course:
        query = query.filter(Enquiry.course.ilike(f"%{course}%"))
        
    return query.order_by(Enquiry.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/enquiries/{enquiry_id}", response_model=EnquiryResponse)
def get_enquiry_by_id(
    enquiry_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Get details of a specific enquiry (Admin only).
    """
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return enquiry


@router.put("/enquiries/{enquiry_id}", response_model=EnquiryResponse)
def update_enquiry_status(
    enquiry_id: int,
    status_in: EnquiryStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Update enquiry status (new -> contacted -> follow_up -> converted -> closed) (Admin only).
    """
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    
    enquiry.status = status_in.status
    db.commit()
    db.refresh(enquiry)
    return enquiry


@router.delete("/enquiries/{enquiry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enquiry(
    enquiry_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> None:
    """
    Delete enquiry record (Admin only).
    """
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    db.delete(enquiry)
    db.commit()


@router.get("/vst-registrations", response_model=List[VSTRegisterResponse])
def list_vst_registrations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    List all VST registrations (Admin only).
    """
    return db.query(VSTRegistration).order_by(VSTRegistration.created_at.desc()).offset(skip).limit(limit).all()
