from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.portfolio import RecommendationStatus

class AllocationRecommendation(Base):
    __tablename__ = "allocation_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("portfolio_profiles.id"), nullable=False)
    
    total_capital = Column(Float, nullable=False)
    cash_reserve = Column(Float, nullable=False)
    available_capital = Column(Float, nullable=False)
    allocated_capital = Column(Float, nullable=False)
    unallocated_capital = Column(Float, nullable=False)
    
    macro_allocation_json = Column(JSON, nullable=False) # { "CRYPTO_SPOT": 5000, "B3_EQUITIES": 3000 }
    rationale_summary = Column(Text, nullable=True)
    status = Column(Enum(RecommendationStatus), nullable=False, default=RecommendationStatus.SUCCESS)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    items = relationship("AllocationItem", back_populates="recommendation", cascade="all, delete-orphan")
