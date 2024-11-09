# app/models/parking_submission.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base
from datetime import datetime

class ParkingSubmission(Base):
    __tablename__ = "parking_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address = Column(String, nullable=False)
    parking_count = Column(Integer, nullable=False)
    permit_required = Column(Boolean, default=False)
    status = Column(String, default="pending")  # possible values: pending, approved, rejected
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship to User
    user = relationship("User", back_populates="parking_submissions")
