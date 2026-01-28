from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.title.asc()).all()


@router.post("/", response_model=CategoryResponse)
async def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

