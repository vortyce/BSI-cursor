from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.enums.signal import SignalDomain

class IndicatorSnapshot(BaseModel):
    rsi: float
    atr: float
    ema200_distance_pct: float

class CandleContext(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float

class TradingViewWebhook(BaseModel):
    payload_version: str = Field(..., examples=["1.0"])
    external_signal_id: str
    domain: Optional[SignalDomain] = Field(default=SignalDomain.CRYPTO_SPOT)
    asset: str
    market: str
    timeframe: str
    signal_type: str
    signal_direction: str
    trigger_price: float
    signal_timestamp: datetime
    strategy_name: str
    strategy_version: str
    indicator_snapshot: IndicatorSnapshot
    candle_context: CandleContext
