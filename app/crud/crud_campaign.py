
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas

def get_campaign(db: Session, campaign_id: int):
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Campaign).offset(skip).limit(limit).all()

def create_campaign(db: Session, campaign: schemas.CampaignCreate):
    db_campaign = models.Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign
