from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.result import Result
from app.models.user import User
from app.schemas.result import ResultCreate, ResultUpdate, ResultResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/results", tags=["Results"])


@router.get("", response_model=List[ResultResponse])
def get_results(
    category: Optional[str] = None,
    featured_only: bool = False,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve achievements/results with optional category filter.
    """
    query = db.query(Result)
    if category:
        query = query.filter(Result.category == category)
    if featured_only:
        query = query.filter(Result.is_featured == True)
        
    return query.order_by(Result.display_order.asc(), Result.id.asc()).all()


@router.get("/{result_id}", response_model=ResultResponse)
def get_result_by_id(result_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Get result details by ID.
    """
    item = db.query(Result).filter(Result.id == result_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Result item not found")
    return item


@router.post("", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
def create_result(
    result_in: ResultCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Create a new student result/achievement (Admin only).
    """
    item = Result(**result_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{result_id}", response_model=ResultResponse)
def update_result(
    result_id: int,
    result_in: ResultUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Update result entry (Admin only).
    """
    item = db.query(Result).filter(Result.id == result_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Result item not found")
    
    for field, value in result_in.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
        
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> None:
    """
    Delete a result entry (Admin only).
    """
    item = db.query(Result).filter(Result.id == result_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Result item not found")
    db.delete(item)
    db.commit()
