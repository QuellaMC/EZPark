# app/api/auth/email_verification.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.user import User
from app.utils.auth import decode_access_token
from app.config.settings import settings

router = APIRouter()

class EmailVerificationResponse(BaseModel):
    message: str

@router.get("/verify-email", response_model=EmailVerificationResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    # Decode the token to get user information
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token."
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token."
        )
    
    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Check if already verified
    if user.is_verified:
        return EmailVerificationResponse(message="Email already verified.")
    
    # Update verification status
    user.is_verified = True
    db.commit()
    db.refresh(user)
    
    return EmailVerificationResponse(message="Email verified successfully.")
