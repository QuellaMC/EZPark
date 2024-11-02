# app/api/parking_spaces/set_full_status.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.parking_space import ParkingSpace
from app.models.user import User
from app.api.utils.permissions import get_current_active_user
from app.config.settings import settings
from datetime import datetime, timedelta

router = APIRouter()

class SetFullStatusRequest(BaseModel):
    is_full: bool = Field(..., example=True)

class SetFullStatusResponse(BaseModel):
    message: str

@router.post("/{parking_space_id}/set-full", response_model=SetFullStatusResponse)
def set_full_status(
    parking_space_id: int,
    request: SetFullStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update the full status of a specific parking space.
    Enforces a cooldown period to prevent rapid status changes.
    """
    # Define the cooldown period
    cooldown_period = timedelta(minutes=settings.cooldown_set_full_status_minutes)
    
    # Check if the user has recently updated a parking space
    if current_user.last_set_full_status_at:
        time_since_last_update = datetime.utcnow() - current_user.last_set_full_status_at
        if time_since_last_update < cooldown_period:
            remaining_time = cooldown_period - time_since_last_update
            minutes, seconds = divmod(remaining_time.seconds, 60)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Cooldown active. Please wait {minutes} minutes and {seconds} seconds before updating again."
            )
    
    # Retrieve the parking space
    parking_space = db.query(ParkingSpace).filter(ParkingSpace.id == parking_space_id).first()
    if not parking_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking space not found."
        )
    
    # Update the status
    parking_space.is_full = request.is_full
    db.commit()
    db.refresh(parking_space)
    
    # Update the user's last_set_full_status_at
    current_user.last_set_full_status_at = datetime.utcnow()
    db.commit()
    
    return SetFullStatusResponse(message="Parking space status updated successfully.")
