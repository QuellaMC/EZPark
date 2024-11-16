# app/api/utils/permissions.py

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth import get_current_active_user

def admin_required(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action."
        )
    return current_user
