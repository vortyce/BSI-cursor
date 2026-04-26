from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from app.db.base import Base
from app.enums.signal import InterpretationStatus, ThesisCategory

class SignalInterpretation(Base):
    __tablename__ = "signal_interpretations"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=False)
    llm_provider = Column(String, nullable=False)
    llm_model = Column(String, nullable=False)
    prompt_version = Column(String, nullable=False)
    status = Column(Enum(InterpretationStatus), default=InterpretationStatus.PROCESSING, nullable=False)
    
    # Resposta bruta real (string) para auditoria máxima
    raw_response_body = Column(Text, nullable=True)
    
    # Campos mapeados do JSON da IA
    regime = Column(String, nullable=True)
    context_alignment = Column(String, nullable=True)
    confidence_level = Column(String, nullable=True)
    confidence_score = Column(Integer, nullable=True)
    profile_fit = Column(String, nullable=True)
    risk_flags_json = Column(JSON, nullable=True)
    primary_thesis = Column(Enum(ThesisCategory), default=ThesisCategory.UNCLEAR_CONTEXT, nullable=False)
    rationale_short = Column(Text, nullable=True)
    rationale_structured_json = Column(JSON, nullable=True)
    
    # Resposta parseada em JSON (se houver sucesso)
    raw_llm_response_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
