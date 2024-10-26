# app/api/admin/config_management.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.config import Config
from app.api.utils.permissions import admin_required

router = APIRouter()

class ConfigResponse(BaseModel):
    smtp_server: Optional[str]
    smtp_port: Optional[int]
    smtp_username: Optional[str]
    smtp_sender: Optional[str]
    frontend_url: Optional[str]
    cooldown_period_minutes: Optional[int]

    class Config:
        orm_mode = True

class UpdateConfigRequest(BaseModel):
    config_key: str = Field(..., example="smtp_server")
    config_value: str = Field(..., example="smtp.newserver.com")

    @validator('config_key')
    def validate_config_key(cls, v):
        allowed_keys = [
            "smtp_server",
            "smtp_port",
            "smtp_username",
            "smtp_sender",
            "frontend_url",
            "cooldown_period_minutes"
        ]
        if v not in allowed_keys:
            raise ValueError("Invalid configuration key.")
        return v

class UpdateConfigResponse(BaseModel):
    message: str

@router.get("/config", response_model=ConfigResponse)
def get_system_config(db: Session = Depends(get_db), current_user = Depends(admin_required)):
    """
    Retrieve the current system configuration settings.
    """
    config = db.query(Config).all()
    config_dict = {item.key: item.value for item in config}
    
    return ConfigResponse(
        smtp_server=config_dict.get("smtp_server"),
        smtp_port=int(config_dict.get("smtp_port")) if config_dict.get("smtp_port") else None,
        smtp_username=config_dict.get("smtp_username"),
        smtp_sender=config_dict.get("smtp_sender"),
        frontend_url=config_dict.get("frontend_url"),
        cooldown_period_minutes=int(config_dict.get("cooldown_period_minutes")) if config_dict.get("cooldown_period_minutes") else None
    )

@router.put("/config", response_model=UpdateConfigResponse)
def update_system_config(
    request: UpdateConfigRequest,
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
    """
    Update specific system configuration parameters.
    """
    config_item = db.query(Config).filter(Config.key == request.config_key).first()
    if not config_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration key not found."
        )
    
    # Type casting based on config_key
    if request.config_key == "smtp_port":
        try:
            config_item.value = int(request.config_value)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid value type for smtp_port. It must be an integer."
            )
    elif request.config_key == "cooldown_period_minutes":
        try:
            config_item.value = int(request.config_value)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid value type for cooldown_period_minutes. It must be an integer."
            )
    else:
        config_item.value = request.config_value
    
    db.commit()
    db.refresh(config_item)
    
    return UpdateConfigResponse(message="Configuration updated successfully.")
