from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    icon = Column(String(100), nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    campaigns = relationship("Campaign", back_populates="category")
