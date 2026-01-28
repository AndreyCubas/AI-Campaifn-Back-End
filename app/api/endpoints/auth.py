from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import User as UserModel
from app.schemas.user import Token, UserCreate
from app.schemas import UserLogin


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        safe_password = user_data.password[:72] if len(user_data.password) > 72 else user_data.password
        hashed_password = get_password_hash(safe_password)

        db_user = UserModel(
            email=user_data.email,
            name=user_data.name,
            password=hashed_password,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "Usuário criado!", "user_id": db_user.id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(userLogin: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == userLogin.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    safe_password = userLogin.password[:72] if len(userLogin.password) > 72 else userLogin.password
    if not verify_password(safe_password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

