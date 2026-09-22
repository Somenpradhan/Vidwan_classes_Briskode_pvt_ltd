from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.gallery import GalleryItem
from app.models.user import User
from app.schemas.gallery import GalleryCreate, GalleryUpdate, GalleryResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("", response_model=List[GalleryResponse])
def get_gallery_items(
    category: Optional[str] = None,
    featured_only: bool = False,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve gallery items. Supports category filter: 'experience', 'student_reviews', 'our_students'.
    """
    query = db.query(GalleryItem)
    if category:
        query = query.filter(GalleryItem.category == category)
    if featured_only:
        query = query.filter(GalleryItem.is_featured == True)
        
    return query.order_by(GalleryItem.display_order.asc(), GalleryItem.id.asc()).all()


@router.get("/{gallery_id}", response_model=GalleryResponse)
def get_gallery_item(gallery_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Get gallery item by ID.
    """
    item = db.query(GalleryItem).filter(GalleryItem.id == gallery_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    return item


@router.post("", response_model=GalleryResponse, status_code=status.HTTP_201_CREATED)
def create_gallery_item(
    gallery_in: GalleryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Add a new item to the gallery (Admin only).
    """
    item = GalleryItem(**gallery_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{gallery_id}", response_model=GalleryResponse)
def update_gallery_item(
    gallery_id: int,
    gallery_in: GalleryUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Update a gallery item (Admin only).
    """
    item = db.query(GalleryItem).filter(GalleryItem.id == gallery_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    
    for field, value in gallery_in.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
        
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{gallery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery_item(
    gallery_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> None:
    """
    Delete a gallery item (Admin only).
    """
    item = db.query(GalleryItem).filter(GalleryItem.id == gallery_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    db.delete(item)
    db.commit()
