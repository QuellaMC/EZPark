# app/models/user.py

from sqlalchemy import Column, Integer, String
from app.utils.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    # Add additional fields as needed, e.g., is_active, is_admin, etc.
