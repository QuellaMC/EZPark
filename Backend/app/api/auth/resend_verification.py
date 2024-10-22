# app/api/auth/resend_verification.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.user import User
from app.utils.email import send_verification_email
from app.config.settings import settings
from datetime import datetime, timedelta

router = APIRouter()

class ResendVerificationRequest(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")

class ResendVerificationResponse(BaseModel):
    message: str

@router.post("/resend-verification", response_model=ResendVerificationResponse)
def resend_verification(request: ResendVerificationRequest, db: Session = Depends(get_db)):
    # Find the user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Check if already verified
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified."
        )
    
    # Check cooldown period
    cooldown_period = timedelta(minutes=settings.cooldown_period_minutes)
    if user.last_verification_email_sent and \
       datetime.utcnow() - user.last_verification_email_sent < cooldown_period:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Please wait before requesting another verification email."
        )
    
    # Send verification email
    try:
        send_verification_email(user.email, user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email."
        )
    
    # Update last verification email sent time
    user.last_verification_email_sent = datetime.utcnow()
    db.commit()
    
    return ResendVerificationResponse(
        message="Verification email resent successfully."
    )
