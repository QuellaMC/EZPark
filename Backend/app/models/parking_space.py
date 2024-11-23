# app/models/parking_space.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.utils.database import Base
from datetime import datetime


class ParkingSpace(Base):
    __tablename__ = "parking_spaces"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False, unique=True)
    parking_count = Column(Integer, nullable=False)
    permit_required = Column(Boolean, default=False)
    is_full = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
