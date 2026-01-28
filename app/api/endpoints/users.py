from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User as UserModel


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def read_users_me(current_user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == int(current_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"id": user.id, "email": user.email, "name": user.name}

