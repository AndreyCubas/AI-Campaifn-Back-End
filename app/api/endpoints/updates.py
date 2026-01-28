from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Campaign, Update
from app.schemas import UpdateCreate, UpdateResponse


router = APIRouter(prefix="/campaigns/{campaign_id}/updates", tags=["updates"])


@router.get("/", response_model=list[UpdateResponse])
async def list_campaign_updates(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return (
        db.query(Update)
        .filter(Update.campaign_id == campaign_id)
        .order_by(Update.created_at.desc())
        .all()
    )


@router.post("/", response_model=UpdateResponse)
async def create_campaign_update(
    campaign_id: int,
    payload: UpdateCreate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    update = Update(campaign_id=campaign_id, **payload.model_dump())
    db.add(update)
    db.commit()
    db.refresh(update)
    return update

