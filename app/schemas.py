from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
import re
from passlib.context import CryptContext  # pip install passlib[bcrypt]

# =================================================
# ENCRYPTION CONTEXT (segurança de senha)
# =================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =================================================
# ENUMS
# =================================================
class StatusEnum(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ApprovalStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class SourceEnum(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    WHATSAPP = "whatsapp"

# =================================================
# USER SCHEMAS (🔒 COM EDIT/SEGURANÇA)
# =================================================
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r"^\(\d{2}\)\d{4,5}-\d{4}$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Senha mínima 8 caracteres")

class UserUpdate(BaseModel):  # ✅ SCHEMA DE EDIÇÃO
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = Field(None, pattern=r"^\(\d{2}\)\d{4,5}-\d{4}$")
    password: Optional[str] = Field(None, min_length=8)  # Nova senha opcional

    @field_validator('password')
    @classmethod
    def hash_password(cls, v: Optional[str]):
        if v:
            return pwd_context.hash(v)
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):  # ✅ LOGIN
    email: EmailStr
    password: str

# =================================================
# CAMPAIGN SCHEMAS (📅 LÓGICA DATA TERMINO)
# =================================================
class CampaignBase(BaseModel):
    title: str = Field(..., min_length=10, max_length=255)
    slug: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    story: Optional[str] = Field(None, max_length=5000)
    cover_image: Optional[str] = Field(None, pattern=r"^https?://")
    goal_amount: Decimal = Field(..., gt=10, le=1000000)
    is_urgent: bool = False
    is_featured: bool = False
    category_id: Optional[int] = None
    status: StatusEnum = StatusEnum.PENDING
    approval_status: ApprovalStatusEnum = ApprovalStatusEnum.PENDING
    source: SourceEnum = SourceEnum.WEB
    end_date: Optional[datetime] = None  # Será validado

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        return re.sub(r'[^a-z0-9]+', '-', v.lower()).strip('-')

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v <= datetime.now():
            raise ValueError('Data de término deve ser futura')
        # Automático: 90 dias se não especificado
        if not v:
            return datetime.now().replace(tzinfo=None) + timedelta(days=90)
        return v

class CampaignCreate(CampaignBase):
    user_id: int

class CampaignUpdate(BaseModel):  # ✅ SCHEMA DE EDIÇÃO
    """Atualização parcial da campanha (PATCH/PUT)"""
    title: Optional[str] = Field(None, min_length=10, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    story: Optional[str] = Field(None, max_length=5000)
    cover_image: Optional[str] = Field(None, pattern=r"^https?://")
    goal_amount: Optional[Decimal] = Field(None, gt=10, le=1000000)
    is_urgent: Optional[bool] = None
    is_featured: Optional[bool] = None
    category_id: Optional[Optional[int]] = None
    end_date: Optional[datetime] = None

class CampaignListResponse(BaseModel):
    id: int
    slug: str
    title: str
    cover_image: Optional[str]
    goal_amount: Decimal
    current_amount: Decimal
    progress_percent: float
    creator_name: str
    category_title: Optional[str]
    is_urgent: bool
    is_featured: bool
    status: StatusEnum

class CampaignResponse(CampaignBase):
    id: int
    user_id: int
    current_amount: Decimal
    progress_percent: float
    creator_name: str
    category_title: Optional[str]
    total_donations: int
    total_updates: int
    updates: List['UpdateResponse'] = []
    model_config = ConfigDict(from_attributes=True)

# Resto dos schemas permanecem iguais...
class DonationBase(BaseModel):
    amount: Decimal = Field(..., gt=1, le=50000)
    donor_name: str = Field(..., min_length=2, max_length=255)
    donor_email: Optional[EmailStr] = None
    is_anonymous: bool = False
    message: Optional[str] = Field(None, max_length=500)

class DonationCreate(DonationBase):
    campaign_id: int

class DonationResponse(DonationBase):
    id: int
    campaign_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UpdateBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    contents: str = Field(..., min_length=20, max_length=2000)

class UpdateCreate(UpdateBase):
    campaign_id: int

class UpdateResponse(UpdateBase):
    id: int
    campaign_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# =================================================
# PAGINAÇÃO
# =================================================
from pydantic import BaseModel
class Pagination(BaseModel):
    page: int = 1
    limit: int = 10
    total: int = 0
    pages: int = 0

class PaginatedCampaigns(BaseModel):
    data: List[CampaignListResponse]
    pagination: Pagination

# Resolve referência circular
CampaignResponse.model_rebuild()
