# app/utils/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Create the SQLAlchemy engine using the DATABASE_URL from settings
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True  # Enables the engine to check the connection's health before using it
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()

def get_db():
    """
    Dependency function that provides a database session.
    It ensures that the session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
