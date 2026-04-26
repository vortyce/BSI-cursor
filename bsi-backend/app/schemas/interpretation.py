from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

class LLMInterpretationResponse(BaseModel):
    regime: Literal["BULLISH_TREND", "BEARISH_TREND", "RANGE", "TRANSITION", "INDETERMINATE"]
    context_alignment: Literal["ALIGNED", "MIXED", "CONFLICTING"]
    confidence_level: Literal["HIGH", "MEDIUM", "LOW"]
    confidence_score: int = Field(ge=0, le=100)
    profile_fit: Literal["CONSERVATIVE", "MODERATE", "AGGRESSIVE", "NONE"]
    risk_flags: List[str]
    rationale_short: str
    rationale_structured: Dict[str, Any]
