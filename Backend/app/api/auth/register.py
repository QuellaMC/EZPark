# app/api/auth/register.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.user import User
from app.utils.auth import get_password_hash
from app.utils.email import send_verification_email
from app.config.settings import settings
import requests

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=8, example="SecurePassword123!")
    recaptcha_token: str = Field(..., example="03AGdBq25...")

class RegisterResponse(BaseModel):
    message: str

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    # Verify reCAPTCHA
    recaptcha_response = request.recaptcha_token
    recaptcha_secret = settings.recaptcha_secret_key
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': recaptcha_secret,
        'response': recaptcha_response
    }
    recaptcha_verification = requests.post(recaptcha_url, data=payload)
    recaptcha_result = recaptcha_verification.json()

    if not recaptcha_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reCAPTCHA verification failed."
        )
    
    # Optionally: reCAPTCHA v3
    # if recaptcha_result.get("score", 0) < 0.5:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="reCAPTCHA verification failed."
    #     )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Hash the password
    hashed_password = get_password_hash(request.password)
    
    # Create the user
    new_user = User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password,
        is_verified=False,
        is_active=True,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send verification email
    try:
        send_verification_email(new_user.email, new_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email."
        )
    
    return RegisterResponse(
        message="Account created successfully. Please check your email to verify your account."
    )
