# app/api/parking_spaces/__init__.py

from fastapi import APIRouter

from .create_parking_space import router as create_parking_space_router
from .set_full_status import router as set_full_status_router
from .list_parking_spaces import router as list_parking_spaces_router
from .get_parking_space_details import router as get_parking_space_details_router

router = APIRouter(
    prefix="/parking-spaces",
    tags=["Parking Spaces"]
)

# Include the individual routers
router.include_router(create_parking_space_router)
router.include_router(set_full_status_router)
router.include_router(list_parking_spaces_router)
router.include_router(get_parking_space_details_router)
