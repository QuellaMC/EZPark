# app/api/auth/verify_email.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.utils.database import get_db
from app.models.user import User
from app.config.settings import settings
from app.utils.auth import decode_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid verification token",
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        sub = payload.get("sub")
        if sub is None or not sub.startswith("verify_email:"):
            logger.warning(f"Invalid token payload: {payload}")
            raise credentials_exception
        user_id = int(sub.split(":")[1])
        logger.debug(f"Decoded user_id from token: {user_id}")
    except (JWTError, ValueError) as e:
        logger.error(f"JWT decoding failed: {e}")
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning(f"User not found for user_id {user_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if user.is_verified:
        logger.info(f"Email already verified for user_id {user_id}")
        return {"message": "Email already verified"}

    user.is_verified = True
    db.commit()
    logger.info(f"Email successfully verified for user_id {user_id}")
    return {"message": "Email successfully verified"}
