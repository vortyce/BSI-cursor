from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.portfolio import PortfolioActionType

class PortfolioActionItem(Base):
    __tablename__ = "portfolio_action_items"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("portfolio_reviews.id"), nullable=False)
    
    # Opcional: Ação sobre posição existente
    position_id = Column(Integer, ForeignKey("portfolio_positions.id"), nullable=True)
    
    # Opcional: Relacionado a um sinal (ex: para REPLACE ou novas entradas)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=True)
    
    action_type = Column(Enum(PortfolioActionType), nullable=False)
    
    # Diferença de score heurístico se for REPLACE (Novo - Atual)
    priority_score_diff = Column(Float, nullable=True)
    
    rationale = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    review = relationship("PortfolioReview", back_populates="actions")
    position = relationship("PortfolioPosition")
    signal = relationship("Signal")
