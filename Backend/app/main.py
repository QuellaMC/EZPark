# app/main.py
from fastapi import FastAPI
from app.api import endpoint1, endpoint2

app = FastAPI(
    title="EZPark Backend",
    description="EZPark Backend API",
    version="1.0.0"
)

app.include_router(endpoint1.router, prefix="/api/endpoint1", tags=["Endpoint1"])
app.include_router(endpoint2.router, prefix="/api/endpoint2", tags=["Endpoint2"])
