from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.portfolio import AllocationStatus

class AllocationItem(Base):
    __tablename__ = "allocation_items"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("allocation_recommendations.id"), nullable=False)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)
    
    suggested_allocation_pct = Column(Float, nullable=False)
    suggested_allocation_amount = Column(Float, nullable=False)
    status = Column(Enum(AllocationStatus), nullable=False)
    
    priority_score = Column(Float, nullable=False)
    priority_score_components = Column(JSON, nullable=False) # { "confidence": 0.4, "alignment": 0.3, ... }
    
    rationale = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    recommendation = relationship("AllocationRecommendation", back_populates="items")
    signal = relationship("Signal")
