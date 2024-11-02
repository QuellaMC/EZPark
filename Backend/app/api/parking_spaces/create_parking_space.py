# app/api/parking_spaces/create_parking_space.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from app.utils.database import get_db
from app.models.parking_space import ParkingSpace
from app.api.utils.permissions import admin_required
from datetime import datetime

router = APIRouter()

class CreateParkingSpaceRequest(BaseModel):
    address: str = Field(..., example="123 Maple Street")
    parking_count: int = Field(..., gt=0, example=20)
    permit_required: bool = Field(..., example=True)

class CreateParkingSpaceResponse(BaseModel):
    id: int
    address: str
    parking_count: int
    permit_required: bool
    is_full: bool
    created_at: str

    class Config:
        orm_mode = True

@router.post("/", response_model=CreateParkingSpaceResponse, status_code=status.HTTP_201_CREATED)
def create_parking_space(
    request: CreateParkingSpaceRequest,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """
    Create a new parking space division.
    """
    # Check if parking space with the same address already exists
    existing_space = db.query(ParkingSpace).filter(ParkingSpace.address == request.address).first()
    if existing_space:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parking space with this address already exists."
        )
    
    # Create new parking space
    new_space = ParkingSpace(
        address=request.address,
        parking_count=request.parking_count,
        permit_required=request.permit_required,
        is_full=False,
        created_at=datetime.utcnow()
    )
    db.add(new_space)
    db.commit()
    db.refresh(new_space)
    
    return new_space
