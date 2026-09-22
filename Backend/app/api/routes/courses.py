from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", response_model=List[CourseResponse])
def get_courses(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve all active courses. Support category filtering.
    """
    query = db.query(Course).filter(Course.is_active == True)
    if category:
        query = query.filter(Course.category == category)
    return query.order_by(Course.display_order.asc(), Course.id.asc()).all()


@router.get("/{course_id_or_slug}", response_model=CourseResponse)
def get_course(
    course_id_or_slug: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get course by ID or slug (e.g. 'nurture', 'qualifier', 'target', '1').
    """
    if course_id_or_slug.isdigit():
        course = db.query(Course).filter(Course.id == int(course_id_or_slug)).first()
    else:
        course = db.query(Course).filter(Course.slug == course_id_or_slug.lower()).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Create a new course (Admin only).
    """
    existing = db.query(Course).filter(Course.slug == course_in.slug.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course with this slug already exists")
    
    course_data = course_in.model_dump()
    course_data["slug"] = course_data["slug"].lower()
    course = Course(**course_data)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Update course (Admin only).
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> None:
    """
    Delete course (Admin only).
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
