from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.decision import UserChoice, SimulatedExecutionStatus

class PortfolioDecision(Base):
    __tablename__ = "portfolio_decisions"

    id = Column(Integer, primary_key=True, index=True)
    action_item_id = Column(Integer, ForeignKey("portfolio_action_items.id"), nullable=False)
    
    user_choice = Column(Enum(UserChoice), nullable=False)
    decision_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user_notes = Column(Text, nullable=True)
    
    simulated_execution_status = Column(Enum(SimulatedExecutionStatus), default=SimulatedExecutionStatus.NONE, nullable=False)
    
    # Snapshot of what changed or would change
    # Ex: { "before": {...}, "after": {...}, "delta": "CLOSED" }
    impact_snapshot_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    action_item = relationship("PortfolioActionItem")
