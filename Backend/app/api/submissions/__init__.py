# app/api/submissions/__init__.py

from fastapi import APIRouter

from .submit_parking_space import router as submit_parking_space_router

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

# Include the individual routers
router.include_router(submit_parking_space_router)
