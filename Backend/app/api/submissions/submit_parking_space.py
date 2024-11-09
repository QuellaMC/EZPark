# app/api/submissions/submit_parking_space.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.utils.database import get_db
from app.models.parking_submission import ParkingSubmission
from app.models.user import User
from app.api.utils.permissions import get_current_active_user
from app.config.settings import settings

router = APIRouter()

class SubmitParkingSpaceRequest(BaseModel):
    address: str = Field(..., example="789 Birch Road")
    parking_count: int = Field(..., gt=0, example=25)
    permit_required: bool = Field(..., example=False)

class SubmitParkingSpaceResponse(BaseModel):
    submission_id: int
    message: str

@router.post("/parking-spaces", response_model=SubmitParkingSpaceResponse, status_code=status.HTTP_201_CREATED)
def submit_parking_space(
    request: SubmitParkingSpaceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Submit a new parking space division request.
    Enforces a cooldown period to prevent rapid submissions.
    """
    # Define the cooldown period
    cooldown_period = timedelta(minutes=settings.cooldown_parking_submission_minutes)
    
    # Check if the user has recently submitted a parking space request
    if current_user.last_parking_submission_at:
        time_since_last_submission = datetime.utcnow() - current_user.last_parking_submission_at
        if time_since_last_submission < cooldown_period:
            remaining_time = cooldown_period - time_since_last_submission
            minutes, seconds = divmod(int(remaining_time.total_seconds()), 60)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Submission cooldown active. Please wait {minutes} minutes and {seconds} seconds before submitting again."
            )
    
    # Check if a submission with the same address already exists and is pending or approved
    existing_submission = db.query(ParkingSubmission).filter(
        ParkingSubmission.address == request.address,
        ParkingSubmission.status.in_(["pending", "approved"])
    ).first()
    if existing_submission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A submission for this address is already pending or approved."
        )
    
    # Create new parking submission
    new_submission = ParkingSubmission(
        user_id=current_user.id,
        address=request.address,
        parking_count=request.parking_count,
        permit_required=request.permit_required,
        status="pending",
        submitted_at=datetime.utcnow()
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    
    # Update the user's last_parking_submission_at
    current_user.last_parking_submission_at = datetime.utcnow()
    db.commit()
    
    return SubmitParkingSpaceResponse(
        submission_id=new_submission.id,
        message="Parking submission submitted successfully and is pending approval."
    )
