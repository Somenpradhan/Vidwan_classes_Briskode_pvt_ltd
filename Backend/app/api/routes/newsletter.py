from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.newsletter import NewsletterSubscriber
from app.models.user import User
from app.schemas.newsletter import NewsletterSubscribeRequest, NewsletterSubscriberResponse
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@router.post("/subscribe", response_model=NewsletterSubscriberResponse, status_code=status.HTTP_201_CREATED)
def subscribe_newsletter(
    sub_in: NewsletterSubscribeRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Subscribe to Vidwan Classes newsletter. Handle existing subscribers idempotently.
    """
    existing = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == sub_in.email.lower()
    ).first()

    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
            db.refresh(existing)
        return existing

    subscriber = NewsletterSubscriber(email=sub_in.email.lower())
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber


@router.get("", response_model=List[NewsletterSubscriberResponse])
def get_newsletter_subscribers(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    """
    Retrieve all newsletter subscribers (Admin only).
    """
    return db.query(NewsletterSubscriber).order_by(NewsletterSubscriber.subscribed_at.desc()).all()
