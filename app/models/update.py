from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Update(Base):
    __tablename__ = "updates"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    contents = Column(String)  # TEXT ilimitado
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    campaign = relationship("Campaign", back_populates="updates")
