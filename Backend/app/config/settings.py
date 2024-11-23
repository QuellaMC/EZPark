# app/config/settings.py

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from datetime import timedelta

class Settings(BaseSettings):
    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # Frontend URL for CORS
    frontend_url: AnyHttpUrl = "http://localhost:3000"

    # Database settings
    database_url: str = "mysql+pymysql://ezpark:testpass@localhost/ezpark_db"  # Replace with your actual database URL

    # JWT settings
    secret_key: str = "your_jwt_secret_key"  # Replace with a secure key
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Rate Limiting
    cooldown_set_full_status_minutes: int = 5
    cooldown_parking_submission_minutes: int = 10

    # SMTP settings for email
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_username: str = "no-reply@example.com"
    smtp_password: str = "your_smtp_password"  # Replace with your SMTP password
    smtp_sender: str = "no-reply@example.com"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
