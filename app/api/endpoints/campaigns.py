from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Campaign
from app.core.database import get_db

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("/")
async def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).offset(skip).limit(limit).all()
    return campaigns
