from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.enums.signal import SignalStatus

class InterpretationShort(BaseModel):
    status: Optional[str] = None
    regime: Optional[str] = None
    confidence_level: Optional[str] = None
    confidence_score: Optional[float] = None
    context_alignment: Optional[str] = None

class OutcomeShort(BaseModel):
    status: str
    return_pct: float

class SignalListItem(BaseModel):
    id: int
    domain: str
    external_signal_id: str
    strategy_name: str
    asset: str
    timeframe: str
    signal_direction: str
    trigger_price: float
    status: SignalStatus
    created_at: datetime
    interpretation: Optional[InterpretationShort] = None
    outcome: OutcomeShort
