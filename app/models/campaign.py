from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    story = Column(String)
    cover_image = Column(String(500))
    goal_amount = Column(Numeric(15,2), nullable=False)
    is_urgent = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    status = Column(String(20), nullable=False)
    approval_status = Column(String(20), nullable=False)
    source = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    

    # Relacionamentos
    user = relationship("User", back_populates="campaigns")
    category = relationship("Category")
    donations = relationship("Donation", back_populates="campaign")
    updates = relationship("Update", back_populates="campaign")
    creator = relationship("User", back_populates="campaigns")