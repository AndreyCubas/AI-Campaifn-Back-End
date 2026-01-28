from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Campaign, Donation
from app.schemas import DonationCreate, DonationResponse


router = APIRouter(prefix="/campaigns/{campaign_id}/donations", tags=["donations"])


@router.get("/", response_model=list[DonationResponse])
async def list_campaign_donations(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return (
        db.query(Donation)
        .filter(Donation.campaign_id == campaign_id)
        .order_by(Donation.created_at.desc())
        .all()
    )


@router.post("/", response_model=DonationResponse)
async def create_campaign_donation(campaign_id: int, payload: DonationCreate, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    donation = Donation(campaign_id=campaign_id, **payload.model_dump())
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

