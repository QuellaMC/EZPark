# app/main.py

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.parking_spaces import router as parking_spaces_router
from app.api.submissions import router as submissions_router
from app.api.utils.rate_limiter import RateLimiterMiddleware
from app.api.utils.logger import logger
from app.utils.database import Base, engine
from app.config.settings import settings
import uvicorn

# 导入所有模型
from app.models import *  # 确保所有模型都已导入

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="EZPark Backend API",
    description="API for managing parking spaces and submissions.",
    version="1.0.0",
    contact={
        "name": "EZPark Support",
        "email": "support@ezpark.com",
    },
    license_info={
        "name": "CC BY-NC-ND 4.0 License",
        "url": "https://github.com/QuellaMC/EZPark/blob/main/LICENSE.md",
    },
)

# Configure CORS
origins = [
    settings.frontend_url,  # e.g., "http://localhost:3000"
    # Add other allowed origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Configure Rate Limiting Middleware
# Example: Limit to 100 requests per minute
app.add_middleware(
    RateLimiterMiddleware,
    max_requests=100,
    window_seconds=60
)

# Include API routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(parking_spaces_router)
app.include_router(submissions_router)

# Lifespan Event Handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("EZPark Backend API is starting up...")
    # Perform startup tasks here (e.g., connect to database)
    yield
    logger.info("EZPark Backend API is shutting down...")
    # Perform shutdown tasks here (e.g., close database connections)

app.router.lifespan = lifespan

# Root Endpoint
@app.get("/", summary="Root Endpoint")
def read_root():
    """
    Root endpoint to verify that the API is running.
    """
    return {"message": "Welcome to the EZPark Backend API. Visit /docs for API documentation."}

# Health Check Endpoint
@app.get("/health", summary="Health Check")
def health_check():
    """
    Health check endpoint to verify that the application is running.
    """
    return {"status": "healthy"}

# Custom Exception Handler (Ensure HTTPException is imported)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for HTTP exceptions to provide consistent error responses.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Run the application (for development purposes)
# In production, use a proper ASGI server like Gunicorn with Uvicorn workers
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True  # Set to False in production
    )
