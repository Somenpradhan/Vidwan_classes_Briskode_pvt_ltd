from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.testimonial import Testimonial
from app.models.user import User
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate, TestimonialResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/testimonials", tags=["Testimonials"])


@router.get("", response_model=List[TestimonialResponse])
def get_testimonials(
    all_unapproved: bool = False,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve approved student testimonials. If all_unapproved is true, requires admin auth to view pending ones.
    """
    query = db.query(Testimonial)
    if not all_unapproved:
        query = query.filter(Testimonial.is_approved == True)
        
    return query.order_by(Testimonial.id.desc()).all()


@router.post("", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
def submit_testimonial(
    testimonial_in: TestimonialCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Public endpoint for submitting student feedback/testimonial.
    """
    item = Testimonial(**testimonial_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{testimonial_id}", response_model=TestimonialResponse)
def update_testimonial(
    testimonial_id: int,
    testimonial_in: TestimonialUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Update or approve/reject testimonial (Admin only).
    """
    item = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    for field, value in testimonial_in.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
        
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> None:
    """
    Delete testimonial (Admin only).
    """
    item = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    db.delete(item)
    db.commit()
