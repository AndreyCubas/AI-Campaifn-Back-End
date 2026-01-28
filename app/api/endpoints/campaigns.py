from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.models import Campaign, Donation
from app.schemas import CampaignCreate, CampaignResponse

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("/", response_model=list[CampaignResponse])
async def list_campaigns(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    category_id: int | None = None,
):
    query = db.query(Campaign)
    if status:
        query = query.filter(Campaign.status == status)
    if category_id:
        query = query.filter(Campaign.category_id == category_id)
    return query.offset(skip).limit(limit).all()


@router.get("/featured", response_model=list[CampaignResponse])
async def featured_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).filter(Campaign.is_featured == True).all()


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return campaign


@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    try:
        import uuid

        data = campaign.model_dump()
        if not data.get("slug"):
            data["slug"] = f"campaign-{uuid.uuid4().hex[:8]}"
        data.setdefault("source", "web")
        data.setdefault("status", "pending")
        data.setdefault("approval_status", "pending")

        db_campaign = Campaign(**data)
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(campaign_id: int, campaign_update: dict, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    for key, value in campaign_update.items():
        setattr(campaign, key, value)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: int,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    db.delete(campaign)
    db.commit()
    return {"message": "Campanha deletada!"}


@router.get("/{campaign_id}/current-amount")
async def get_campaign_current_amount(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    total = (
        db.query(func.coalesce(func.sum(Donation.amount), 0))
        .filter(Donation.campaign_id == campaign_id)
        .scalar()
    )
    return {"campaign_id": campaign_id, "current_amount": float(total)}
