from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DonationCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    donor_name: str = Field(..., min_length=2, max_length=255)
    donor_email: Optional[EmailStr] = None
    is_anonymous: bool = False


class DonationResponse(BaseModel):
    id: int
    campaign_id: int
    amount: Decimal
    donor_name: str
    donor_email: Optional[EmailStr] = None
    is_anonymous: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

