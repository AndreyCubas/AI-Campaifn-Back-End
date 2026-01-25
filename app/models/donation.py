from sqlalchemy import Column, Integer, Numeric, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    donor_name = Column(String(255), nullable=False)
    donor_email = Column(String(255))
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    campaign = relationship("Campaign", back_populates="donations")
