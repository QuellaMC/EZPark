# app/api/parking_spaces/get_parking_space_details.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.parking_space import ParkingSpace

router = APIRouter()

class ParkingSpaceDetailResponse(BaseModel):
    id: int
    address: str
    parking_count: int
    permit_required: bool
    is_full: bool
    created_at: str

    class Config:
        from_attributes = True

@router.get("/{parking_space_id}", response_model=ParkingSpaceDetailResponse)
def get_parking_space_details(
    parking_space_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve detailed information about a specific parking space.
    """
    parking_space = db.query(ParkingSpace).filter(ParkingSpace.id == parking_space_id).first()
    if not parking_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking space not found."
        )
    
    return parking_space
