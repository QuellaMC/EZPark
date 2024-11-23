# app/api/admin/parking_submission_management.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.parking_submission import ParkingSubmission
from app.api.utils.permissions import admin_required
from datetime import datetime

router = APIRouter()

class ParkingSubmissionResponse(BaseModel):
    submission_id: int
    user_id: int
    address: str
    parking_count: int
    permit_required: bool
    status: str
    submitted_at: str

    class Config:
        from_attributes = True

class ReviewSubmissionRequest(BaseModel):
    status: str = Field(..., example="approved")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "approved"
            }
        }

class ReviewSubmissionResponse(BaseModel):
    message: str

@router.get("/parking-submissions", response_model=List[ParkingSubmissionResponse])
def get_parking_submissions(db: Session = Depends(get_db), current_user = Depends(admin_required)):
    """
    Retrieve all parking space submissions pending review.
    """
    submissions = db.query(ParkingSubmission).filter(ParkingSubmission.status == "pending").all()
    return submissions

@router.put("/parking-submissions/{submission_id}", response_model=ReviewSubmissionResponse)
def review_parking_submission(
    submission_id: int,
    request: ReviewSubmissionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """
    Approve or reject a specific parking space submission.
    """
    if request.status not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status value."
        )
    
    submission = db.query(ParkingSubmission).filter(ParkingSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found."
        )
    
    if submission.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission has already been reviewed."
        )
    
    submission.status = request.status
    submission.reviewed_at = datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(submission)
    
    return ReviewSubmissionResponse(message=f"Parking submission {request.status} successfully.")
