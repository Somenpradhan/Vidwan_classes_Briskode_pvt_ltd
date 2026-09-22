from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.faculty import Faculty
from app.models.user import User
from app.schemas.faculty import FacultyCreate, FacultyUpdate, FacultyResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/faculty", tags=["Faculty"])


@router.get("", response_model=List[FacultyResponse])
def get_faculty(db: Session = Depends(get_db)) -> Any:
    """
    Retrieve all active faculty members sorted by display order.
    """
    return db.query(Faculty).filter(Faculty.is_active == True).order_by(Faculty.display_order.asc(), Faculty.id.asc()).all()


@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty_member(faculty_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Get faculty member by ID.
    """
    member = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    return member


@router.post("", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
def create_faculty(
    faculty_in: FacultyCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Create a new faculty member (Admin only).
    """
    member = Faculty(**faculty_in.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.put("/{faculty_id}", response_model=FacultyResponse)
def update_faculty(
    faculty_id: int,
    faculty_in: FacultyUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Update faculty member details (Admin only).
    """
    member = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    for field, value in faculty_in.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
        
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> None:
    """
    Delete a faculty member (Admin only).
    """
    member = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    db.delete(member)
    db.commit()
