from typing import Any
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.vst_registration import VSTRegistration
from app.schemas.vst import VSTRegisterRequest, VSTRegisterResponse
from app.services.email_service import send_vst_registration_notification

router = APIRouter(prefix="/vst", tags=["VST"])


@router.post("/register", response_model=VSTRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_vst(
    vst_in: VSTRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Any:
    """
    Vidwan Scholarship Test (VST) Registration.
    Checks for duplicate registrations by phone & email, saves to DB, sends notification emails.
    """
    existing = db.query(VSTRegistration).filter(
        (VSTRegistration.email == vst_in.email) | (VSTRegistration.phone == vst_in.phone)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="A registration with this email or phone number already exists for VST."
        )

    vst_reg = VSTRegistration(**vst_in.model_dump())
    db.add(vst_reg)
    db.commit()
    db.refresh(vst_reg)

    vst_data = vst_in.model_dump()
    background_tasks.add_task(send_vst_registration_notification, vst_data)

    return vst_reg
