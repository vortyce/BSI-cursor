from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.portfolio import PositionStatus

class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)
    
    entry_price = Column(Float, nullable=False)
    allocated_capital = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    
    status = Column(Enum(PositionStatus), default=PositionStatus.ACTIVE, nullable=False)
    entry_rationale = Column(Text, nullable=True)
    
    # Track when the user last acknowledged an action suggestion for this position
    acknowledged_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    signal = relationship("Signal")
