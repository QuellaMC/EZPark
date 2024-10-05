# app/main.py

from fastapi import FastAPI
from app.api import endpoint1, endpoint2, authentication  # Import the authentication router
from app.utils.database import Base, engine
from app.models import user  # Ensure all models are imported to create tables

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EZPark Backend",
    description="Backend API for EZPark website",
    version="1.0.0"
)

# Include API routers
app.include_router(endpoint1.router, prefix="/api/endpoint1", tags=["Endpoint1"])
# app.include_router(endpoint2.router, prefix="/api/endpoint2", tags=["Endpoint2"])
app.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
