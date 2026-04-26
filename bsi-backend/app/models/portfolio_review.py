from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.portfolio import RecommendationStatus, ConcentrationStatus

class PortfolioReview(Base):
    __tablename__ = "portfolio_reviews"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("portfolio_profiles.id"), nullable=False)
    
    # Diagnóstico (Snapshot)
    total_market_value = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    
    # Drift analysis per domain and per position
    # Ex: { "domains": { "CRYPTO": 5.2 }, "positions": { "BTC": 1.2 } }
    drift_analysis_json = Column(JSON, nullable=False)
    
    concentration_status = Column(Enum(ConcentrationStatus), nullable=False)
    
    # Recomendação de Ação (Resumo)
    status = Column(Enum(RecommendationStatus), nullable=False)
    summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    profile = relationship("PortfolioProfile")
    actions = relationship("PortfolioActionItem", back_populates="review")
