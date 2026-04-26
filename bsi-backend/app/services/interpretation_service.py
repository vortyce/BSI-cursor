from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.enums.signal import SignalStatus, InterpretationStatus, SignalDomain
from app.integrations.llm.factory import LLMClientFactory
from app.schemas.interpretation import LLMInterpretationResponse
from app.core.config import settings
from app.core.prompts import BSI_SYSTEM_PROMPT, BSI_USER_PROMPT_TEMPLATE, B3_EQUITIES_USER_PROMPT_TEMPLATE
from app.core.market_context import get_market_session, get_session_label
from app.core.logging_utils import get_logger
from app.core.errors import NotFoundError

logger = get_logger("interpretation")

class InterpretationService:
    def __init__(self, db: Session):
        self.db = db
        # Fábrica desacoplada
        self.llm_client = LLMClientFactory.get_client()

    def process_pending_signals(self):
        # Sinais STORED são os candidatos (técnicos e aguardando IA)
        signals = self.db.query(Signal).filter(Signal.status == SignalStatus.STORED).all()
        results = []
        for signal in signals:
            results.append(self.interpret_signal(signal))
        return results

    def process_pending_signals_data(self):
        results = self.process_pending_signals()
        return {"processed_count": len(results), "results": results}

    def interpret_signal_by_id(self, signal_id: int):
        signal = self.db.query(Signal).filter(Signal.id == signal_id).first()
        if not signal:
            raise NotFoundError("Signal not found", domain="interpretations")
        return self.interpret_signal(signal)

    def interpret_signal(self, signal: Signal):
        # 1. POLÍTICA DE IDEMPOTÊNCIA: Se já interpretado com sucesso, ignora.
        if signal.status == SignalStatus.INTERPRETED:
            return {"status": "skipped", "reason": "already_interpreted", "signal_id": signal.id}

        interpretation = SignalInterpretation(
            signal_id=signal.id,
            llm_provider=settings.DEFAULT_LLM_PROVIDER,
            llm_model=settings.DEFAULT_LLM_MODEL,
            prompt_version=settings.PROMPT_VERSION,
            status=InterpretationStatus.PROCESSING
        )
        self.db.add(interpretation)
        self.db.flush()

        try:
            # 3. Montagem do Prompt (Baseada em Domínio)
            if signal.domain == SignalDomain.B3_EQUITIES:
                session = get_market_session(signal.signal_timestamp, signal.domain)
                user_prompt = B3_EQUITIES_USER_PROMPT_TEMPLATE.format(
                    direction=signal.signal_direction,
                    price=signal.trigger_price,
                    asset=signal.asset,
                    indicators=signal.indicator_snapshot_json,
                    context=signal.candle_context_json,
                    market_session=session.value,
                    market_session_label=get_session_label(session)
                )
            else:
                user_prompt = BSI_USER_PROMPT_TEMPLATE.format(
                    direction=signal.signal_direction,
                    price=signal.trigger_price,
                    asset=signal.asset,
                    indicators=signal.indicator_snapshot_json,
                    context=signal.candle_context_json
                )

            # 4. Chamada ao Provedor
            data_dict, raw_content = self.llm_client.get_interpretation(BSI_SYSTEM_PROMPT, user_prompt)
            
            # SALVAMENTO BRUTO REAL (String da API)
            interpretation.raw_response_body = raw_content
            
            # 5. Validação com Pydantic
            try:
                validated_data = LLMInterpretationResponse(**data_dict)
                
                # Sucesso: Persistência estruturada
                interpretation.raw_llm_response_json = data_dict
                interpretation.regime = validated_data.regime
                interpretation.context_alignment = validated_data.context_alignment
                interpretation.confidence_level = validated_data.confidence_level
                interpretation.confidence_score = validated_data.confidence_score
                interpretation.profile_fit = validated_data.profile_fit
                interpretation.risk_flags_json = validated_data.risk_flags
                interpretation.rationale_short = validated_data.rationale_short
                interpretation.rationale_structured_json = validated_data.rationale_structured
                
                interpretation.status = InterpretationStatus.SUCCESS
                signal.status = SignalStatus.INTERPRETED # SINAL SÓ MUDA NO SUCESSO
                
            except ValidationError as ve:
                logger.warning("validate_llm_response", f"Invalid LLM response schema for signal {signal.id}: {str(ve)}")
                interpretation.status = InterpretationStatus.INVALID_RESPONSE
                interpretation.rationale_short = f"Schema Validation Error: {str(ve)}"
                # O sinal permanece STORED (usável tecnicamente)
            
            self.db.commit()
            return {"status": "success", "signal_id": signal.id, "interpretation_id": interpretation.id}

        except Exception as e:
            logger.error("interpret_signal", f"Error calling LLM for signal {signal.id}: {str(e)}")
            interpretation.status = InterpretationStatus.FAILED
            interpretation.raw_response_body = f"Infrastructure Error: {str(e)}"
            self.db.commit()
            return {"status": "failed", "signal_id": signal.id, "error": str(e)}
