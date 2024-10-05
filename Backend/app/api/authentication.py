# app/api/authentication.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import auth
from app.utils.database import get_db
from app.models.user import User

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and return a JWT token.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=dict)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    """
    Endpoint to retrieve the current authenticated user's information.
    """
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}
