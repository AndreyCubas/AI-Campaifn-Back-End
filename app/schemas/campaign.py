from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

# Para CREATE (sem ID)
class CampaignCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    story: Optional[str] = None
    goal_amount: Decimal
    category_id: int
    user_id: int
    cover_image: Optional[str] = None
    end_date: Optional[datetime] = None

# Para READ (com todos campos)
class CampaignResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str]
    story: Optional[str]
    cover_image: Optional[str]
    goal_amount: Decimal
    current_amount: Decimal
    user_id: int
    category_id: Optional[int]
    is_urgent: bool = False
    is_featured: bool = False
    status: str
    approval_status: str
    created_at: datetime
    end_date: Optional[datetime]

    class Config:
        from_attributes = True  # Para SQLAlchemy

# Lista de campaigns
CampaignList = List[CampaignResponse]
