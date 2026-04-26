from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.enums.portfolio import RiskProfile, PrimaryGoal, TimeHorizon, ManagementStyle, PositionStatus, PortfolioActionType
from app.enums.decision import UserChoice

class ProfileDTO(BaseModel):
    initial_capital: float
    risk_profile: RiskProfile
    primary_goal: PrimaryGoal
    horizon: TimeHorizon
    allowed_domains: List[str]
    max_single_position_pct: float
    max_domain_exposure_pct: float
    keep_cash_reserve_pct: float
    management_style: ManagementStyle

class DecisionRequestDTO(BaseModel):
    action_item_id: int
    choice: UserChoice
    notes: Optional[str] = None

class PortfolioPositionDTO(BaseModel):
    id: int
    signal_id: Optional[int]
    asset: str
    domain: str
    entry_price: float
    allocated_capital: float
    status: PositionStatus
    entry_rationale: Optional[str]
    acknowledged_at: Optional[datetime]
    created_at: datetime

class ActionItemDTO(BaseModel):
    id: int
    action_type: PortfolioActionType
    asset: str
    priority_score_diff: float
    rationale: str
    position_id: Optional[int]

class RecommendationDTO(BaseModel):
    id: int
    total_capital: float
    cash_reserve: float
    available_capital: float
    allocated_capital: float
    unallocated_capital: float
    macro_allocation_json: Dict[str, Any]
    rationale_summary: str
    status: str
    created_at: datetime
    items: List[Dict[str, Any]] # Will refine if needed

class PortfolioReviewDTO(BaseModel):
    id: int
    total_market_value: float
    cash_balance: float
    drift_analysis_json: Dict[str, Any]
    concentration_status: str
    status: str
    summary: str
    created_at: datetime
    actions: List[ActionItemDTO]
