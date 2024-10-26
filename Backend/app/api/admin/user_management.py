# app/api/admin/user_management.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.user import User
from app.api.utils.permissions import admin_required

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    is_admin: bool
    created_at: str

    class Config:
        orm_mode = True

class UpdateUserStatusRequest(BaseModel):
    is_active: bool = Field(..., example=True)

class UpdateUserStatusResponse(BaseModel):
    message: str

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    """
    Retrieve a list of all users.
    """
    users = db.query(User).all()
    return users

@router.put("/users/{user_id}", response_model=UpdateUserStatusResponse)
def update_user_status(
    user_id: int,
    request: UpdateUserStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    """
    Update the active status of a specified user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    user.is_active = request.is_active
    db.commit()
    db.refresh(user)
    
    return UpdateUserStatusResponse(message="User status updated successfully.")
