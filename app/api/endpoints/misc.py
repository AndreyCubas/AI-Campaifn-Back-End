from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Campaign


router = APIRouter(tags=["misc"])


@router.get("/")
async def root():
    return {"message": "API funcionando!"}


@router.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"status": "PostgreSQL OK", "result": result}


@router.get("/health")
async def health():
    return {"status": "OK", "version": "1.0.0"}


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_campaigns = db.query(Campaign).count()
    active_campaigns = db.query(Campaign).filter(Campaign.status == "active").count()
    return {"total": total_campaigns, "active": active_campaigns}

