# app/config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    database_url: str
    
    # Authentication settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30  # Token expiry time in minutes
    
    # Additional settings can be added here
    # Example:
    # debug: bool = False
    # api_prefix: str = "/api"
    
    # Validators (if needed)
    @validator("database_url")
    def validate_database_url(cls, v):
        if not v.startswith("mysql+pymysql://"):
            raise ValueError("DATABASE_URL must start with 'mysql+pymysql://'")
        return v
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
