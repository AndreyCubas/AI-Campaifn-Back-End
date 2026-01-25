from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, Base, get_db
from app.core.security import get_current_user, verify_password, get_password_hash 
from app.schemas.user import UserCreate, Token  
from app.models import *  
from app.models import User as UserModel


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
async def delete_campaign(
    campaign_id: int, 
    current_user_id: str = Depends(get_current_user),  # ← PROTEGIDO!
    db: Session = Depends(get_db)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return {"error": "Campanha não encontrada"}
    
    db.delete(campaign)
    db.commit()
    return {"message": "Campanha deletada!"}

# FILTROS
@app.get("/campaigns/featured")
async def get_featured(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).filter(Campaign.is_featured == True).all()
    return campaigns



# REGISTER
@app.post("/auth/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verifica se usuário já existe
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        return {"error": "Email já cadastrado"}
    
    # Cria usuário criptografado
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        name=user_data.name,
        password=hashed_password,  # Campo password no model
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuário criado!", "user_id": db_user.id}

# LOGIN
@app.post("/auth/login", response_model=Token)
async def login(form_data: dict, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data["email"]).first()
    if not user or not verify_password(form_data["password"], user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# PERFIL (PROTEGIDO)
@app.get("/users/me")
async def read_users_me(current_user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"id": user.id, "email": user.email, "name": user.name}
