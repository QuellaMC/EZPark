# app/config/settings.py

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from datetime import timedelta

class Settings(BaseSettings):
    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = 8888

    # Frontend URL for CORS
    frontend_url: AnyHttpUrl = "https://ezpark.aicg.tech"

    # Database settings
    database_url: str = "mysql+pymysql://ezpark_backend:PASSWORD@localhost/ezpark_backend"

    # JWT settings
    jwt_secret_key: str = "KEY"  # Replace with a secure key
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Rate Limiting
    cooldown_set_full_status_minutes: int = 5
    cooldown_parking_submission_minutes: int = 10
    cooldown_period_minutes: int = 1

    # SMTP settings for email
    smtp_server: str = "smtp.test.com"
    smtp_port: int = 465
    smtp_username: str = "noreply@test.com"
    smtp_password: str = "test.com"  # Replace with your SMTP password
    smtp_sender: str = "noreply@test.com"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
