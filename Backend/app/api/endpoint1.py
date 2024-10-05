# app/api/endpoint1.py
from fastapi import APIRouter, Depends
from app.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
async def read_endpoint1(db: Session = Depends(get_db)):
    # 处理逻辑
    return {"message": "Endpoint1 data"}
