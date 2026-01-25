from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, Base, get_db
from app.models import *  # ✅ IMPORTA TUDO do __init__.py

app = FastAPI(title="Crowdfunding API 🚀")
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "✅ API funcionando!"}

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"status": "✅ PostgreSQL OK", "result": result}

@app.get("/campaigns")
async def get_campaigns(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    campaigns = db.query(Campaign).offset(skip).limit(limit).all()
    return campaigns

@app.post("/campaigns")
async def create_campaign(campaign: dict, db: Session = Depends(get_db)):
    """Cria nova campanha com slug automático"""
    try:
        import uuid
        campaign['slug'] = campaign.get('slug', f"campanha-{uuid.uuid4().hex[:8]}")
        campaign['source'] = campaign.get('source', 'web')
        campaign['status'] = campaign.get('status', 'pending')
        campaign['approval_status'] = campaign.get('approval_status', 'pending')
        
        db_campaign = Campaign(**campaign)
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    except Exception as e:
        return {"error": str(e)}


# GET campanha por ID
@app.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return {"error": "Campanha não encontrada"}
    return campaign

# PUT editar campanha
@app.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int, campaign_update: dict, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return {"error": "Campanha não encontrada"}
    
    for key, value in campaign_update.items():
        setattr(campaign, key, value)
    
    db.commit()
    db.refresh(campaign)
    return campaign

# DELETE campanha
@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return {"error": "Campanha não encontrada"}
    
    db.delete(campaign)
    db.commit()
    return {"message": "Campanha deletada!"}

# FILTROS (bonus)
@app.get("/campaigns/featured")
async def get_featured(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).filter(Campaign.is_featured == True).all()
    return campaigns
