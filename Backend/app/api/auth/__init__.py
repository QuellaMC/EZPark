# app/api/auth/__init__.py

from fastapi import APIRouter

from .register import router as register_router
from .login import router as login_router
from .email_verification import router as email_verification_router
from .resend_verification import router as resend_verification_router

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Include the individual routers
router.include_router(register_router)
router.include_router(login_router)
router.include_router(email_verification_router)
router.include_router(resend_verification_router)
