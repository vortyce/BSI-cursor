from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from app.db.base import Base
from app.enums.signal import RawWebhookParseStatus

class RawWebhookLog(Base):
    __tablename__ = "raw_webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String, nullable=False, default="tradingview")
    raw_body = Column(Text, nullable=False)
    headers_json = Column(JSON, nullable=True)
    http_status_to_sender = Column(Integer, nullable=True)
    parse_status = Column(Enum(RawWebhookParseStatus), nullable=False, default=RawWebhookParseStatus.RECEIVED)
    parse_error_message = Column(Text, nullable=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
