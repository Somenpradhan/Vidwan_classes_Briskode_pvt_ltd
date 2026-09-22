from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class NewsletterSubscribeRequest(BaseModel):
    email: EmailStr


class NewsletterSubscriberResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    subscribed_at: datetime

    model_config = ConfigDict(from_attributes=True)
