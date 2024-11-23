# app/api/parking_spaces/list_parking_spaces.py

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.parking_space import ParkingSpace

router = APIRouter()

class ParkingSpaceResponse(BaseModel):
    id: int
    address: str
    parking_count: int
    permit_required: bool
    is_full: bool
    created_at: str

    class Config:
        from_attributes = True

class ListParkingSpacesResponse(BaseModel):
    parking_spaces: List[ParkingSpaceResponse]
    total: int
    page: int
    limit: int

@router.get("/", response_model=ListParkingSpacesResponse)
def list_parking_spaces(
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(10, gt=0, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all parking spaces with pagination.
    """
    total = db.query(ParkingSpace).count()
    parking_spaces = db.query(ParkingSpace).offset((page - 1) * limit).limit(limit).all()
    
    return ListParkingSpacesResponse(
        parking_spaces=parking_spaces,
        total=total,
        page=page,
        limit=limit
    )
