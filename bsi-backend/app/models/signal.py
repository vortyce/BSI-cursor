from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from app.db.base import Base
from app.enums.signal import SignalStatus

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    raw_log_id = Column(Integer, ForeignKey("raw_webhook_logs.id"), nullable=False)
    payload_version = Column(String, nullable=False)
    external_signal_id = Column(String, unique=True, nullable=False, index=True)
    domain = Column(String, nullable=False, default="CRYPTO_SPOT")
    asset = Column(String, nullable=False)
    market = Column(String, nullable=False)
    timeframe = Column(String, nullable=False)
    signal_type = Column(String, nullable=False)
    signal_direction = Column(String, nullable=False)
    trigger_price = Column(Float, nullable=False)
    signal_timestamp = Column(DateTime, nullable=False)
    strategy_name = Column(String, nullable=False)
    strategy_version = Column(String, nullable=False)
    indicator_snapshot_json = Column(JSON, nullable=False)
    candle_context_json = Column(JSON, nullable=False)
    status = Column(Enum(SignalStatus), nullable=False, default=SignalStatus.RECEIVED)
    status_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
