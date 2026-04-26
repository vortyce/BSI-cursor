from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Enum
from app.db.base import Base
from app.enums.portfolio import RiskProfile, PrimaryGoal, TimeHorizon, ManagementStyle

class PortfolioProfile(Base):
    __tablename__ = "portfolio_profiles"

    id = Column(Integer, primary_key=True, index=True)
    initial_capital = Column(Float, nullable=False)
    risk_profile = Column(Enum(RiskProfile), nullable=False, default=RiskProfile.MODERATE)
    primary_goal = Column(Enum(PrimaryGoal), nullable=False, default=PrimaryGoal.GROWTH)
    horizon = Column(Enum(TimeHorizon), nullable=False, default=TimeHorizon.MEDIUM)
    allowed_domains = Column(JSON, nullable=False) # e.g. ["CRYPTO_SPOT", "B3_EQUITIES"]
    max_single_position_pct = Column(Float, nullable=False, default=10.0)
    max_domain_exposure_pct = Column(Float, nullable=False, default=50.0)
    keep_cash_reserve_pct = Column(Float, nullable=False, default=20.0)
    management_style = Column(Enum(ManagementStyle), nullable=False, default=ManagementStyle.TACTICAL)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
