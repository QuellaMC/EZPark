# app/api/admin/__init__.py

from fastapi import APIRouter

from .user_management import router as user_management_router
from .parking_submission_management import router as parking_submission_management_router
from .config_management import router as config_management_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# Include the individual routers
router.include_router(user_management_router)
router.include_router(parking_submission_management_router)
router.include_router(config_management_router)
