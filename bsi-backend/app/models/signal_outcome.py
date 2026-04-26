from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from app.db.base import Base
from app.enums.signal import DataSourceQuality

class SignalOutcome(Base):
    __tablename__ = "signal_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False, unique=True)
    
    # Taxonomia
    outcome_status = Column(String, nullable=False) # WIN, LOSS, BREAKEVEN, OPEN, EXPIRED, INCONCLUSIVE
    evaluation_method = Column(String, nullable=False) # e.g., "TRADINGVIEW_STRATEGY_FOLLOWUP"
    data_quality = Column(Enum(DataSourceQuality), default=DataSourceQuality.REAL_CAPTURED, nullable=False)
    
    # Dados de Execução e Preço
    entry_reference_price = Column(Float, nullable=False)
    resolution_price = Column(Float, nullable=True)
    max_favorable_excursion_pct = Column(Float, nullable=True) # MFE %
    max_adverse_excursion_pct = Column(Float, nullable=True)   # MAE %
    final_return_pct = Column(Float, nullable=True)
    
    # Tempo
    bars_to_resolution = Column(Integer, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Metadados
    notes = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
