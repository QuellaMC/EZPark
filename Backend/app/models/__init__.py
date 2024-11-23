# app/models/__init__.py

from .user import User
from .parking_submission import ParkingSubmission
from .parking_space import ParkingSpace
from .config import Config

__all__ = ["User", "ParkingSubmission", "ParkingSpace", "Config"]
