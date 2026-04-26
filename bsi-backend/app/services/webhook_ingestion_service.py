from sqlalchemy.orm import Session
from app.models.raw_webhook_log import RawWebhookLog
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.models.signal_outcome import SignalOutcome
from app.enums.signal import RawWebhookParseStatus, SignalStatus, SignalDomain
from app.core.errors import NotFoundError
from app.core.logging_utils import get_logger
from app.schemas.webhook import TradingViewWebhook

logger = get_logger("webhooks")

class WebhookIngestionService:
    def __init__(self, db: Session):
        self.db = db

    def process_webhook(self, payload: TradingViewWebhook, raw_body: str = "{}", headers: dict = {}, source: str = "tradingview"):
        signal_domain = payload.domain or SignalDomain.CRYPTO_SPOT

        try:
            raw_log = RawWebhookLog(
                source=source,
                raw_body=raw_body,
                headers_json=headers,
                parse_status=RawWebhookParseStatus.RECEIVED,
                http_status_to_sender=202
            )
            self.db.add(raw_log)
            self.db.flush()

            existing = self.db.query(Signal).filter(Signal.external_signal_id == payload.external_signal_id).first()
            if existing:
                raw_log.parse_status = RawWebhookParseStatus.DUPLICATE_SIGNAL
                raw_log.signal_id = existing.id
                self.db.commit()
                return {"status": "duplicate", "signal_id": existing.id, "raw_log_id": raw_log.id}

            signal = Signal(
                raw_log_id=raw_log.id,
                payload_version=payload.payload_version,
                external_signal_id=payload.external_signal_id,
                domain=signal_domain.value,
                asset=payload.asset,
                market=payload.market,
                timeframe=payload.timeframe,
                signal_type=payload.signal_type,
                signal_direction=payload.signal_direction,
                trigger_price=payload.trigger_price,
                signal_timestamp=payload.signal_timestamp,
                strategy_name=payload.strategy_name,
                strategy_version=payload.strategy_version,
                indicator_snapshot_json=payload.indicator_snapshot.model_dump(),
                candle_context_json=payload.candle_context.model_dump(),
                status=SignalStatus.STORED,
                status_message="Signal stored successfully"
            )

            self.db.add(signal)
            self.db.flush()

            raw_log.signal_id = signal.id
            raw_log.parse_status = RawWebhookParseStatus.SIGNAL_CREATED
            self.db.commit()

            return {"status": "accepted", "signal_id": signal.id, "raw_log_id": raw_log.id}

        except Exception as e:
            self.db.rollback()
            logger.error("process_webhook", f"Unexpected webhook ingestion error: {str(e)}")
            return {"status": "error", "reason": "internal_error", "raw_log_id": None}

    def list_signals(self, domain: str = None):
        query = self.db.query(Signal)
        if domain:
            query = query.filter(Signal.domain == domain)

        signals = query.order_by(Signal.created_at.desc()).limit(100).all()
        return [self._serialize_signal_list_item(signal) for signal in signals]

    def get_signal_full_detail(self, signal_id: int):
        signal = self.db.query(Signal).filter(Signal.id == signal_id).first()
        if not signal:
            raise NotFoundError("Sinal não encontrado", domain="webhooks")

        interpretation = self._latest_interpretation(signal.id)
        outcome = self.db.query(SignalOutcome).filter(SignalOutcome.signal_id == signal.id).first()

        return {
            "id": signal.id,
            "domain": signal.domain,
            "external_signal_id": signal.external_signal_id,
            "asset": signal.asset,
            "market": signal.market,
            "timeframe": signal.timeframe,
            "signal_type": signal.signal_type,
            "signal_direction": signal.signal_direction,
            "trigger_price": signal.trigger_price,
            "signal_timestamp": signal.signal_timestamp,
            "strategy_name": signal.strategy_name,
            "strategy_version": signal.strategy_version,
            "indicator_snapshot_json": signal.indicator_snapshot_json,
            "candle_context_json": signal.candle_context_json,
            "status": signal.status,
            "created_at": signal.created_at,
            "updated_at": signal.updated_at,
            "interpretation_full": self._serialize_interpretation_detail(interpretation),
            "outcome_full": self._serialize_outcome_detail(outcome, signal),
        }

    def _serialize_signal_list_item(self, signal: Signal):
        interpretation = self._latest_interpretation(signal.id)
        outcome = self.db.query(SignalOutcome).filter(SignalOutcome.signal_id == signal.id).first()

        return {
            "id": signal.id,
            "domain": signal.domain,
            "external_signal_id": signal.external_signal_id,
            "strategy_name": signal.strategy_name,
            "asset": signal.asset,
            "timeframe": signal.timeframe,
            "signal_direction": signal.signal_direction,
            "trigger_price": signal.trigger_price,
            "status": signal.status,
            "created_at": signal.created_at,
            "interpretation": self._serialize_interpretation_summary(interpretation),
            "outcome": {
                "status": outcome.outcome_status if outcome else "OPEN",
                "return_pct": outcome.final_return_pct if outcome else 0,
            },
        }

    def _latest_interpretation(self, signal_id: int):
        return self.db.query(SignalInterpretation).filter(
            SignalInterpretation.signal_id == signal_id
        ).order_by(SignalInterpretation.created_at.desc()).first()

    @staticmethod
    def _serialize_interpretation_summary(interpretation):
        if not interpretation:
            return None
        return {
            "status": interpretation.status,
            "regime": interpretation.regime,
            "confidence_level": interpretation.confidence_level,
            "confidence_score": interpretation.confidence_score,
            "context_alignment": interpretation.context_alignment,
        }

    @staticmethod
    def _serialize_interpretation_detail(interpretation):
        if not interpretation:
            return None
        return {
            "llm_provider": interpretation.llm_provider,
            "llm_model": interpretation.llm_model,
            "prompt_version": interpretation.prompt_version,
            "status": interpretation.status,
            "regime": interpretation.regime,
            "context_alignment": interpretation.context_alignment,
            "confidence_level": interpretation.confidence_level,
            "confidence_score": interpretation.confidence_score,
            "profile_fit": interpretation.profile_fit,
            "risk_flags": interpretation.risk_flags_json if interpretation.risk_flags_json else [],
            "rationale_short": interpretation.rationale_short,
            "rationale_structured": interpretation.rationale_structured_json,
            "raw_response_body": interpretation.raw_response_body,
        }

    @staticmethod
    def _serialize_outcome_detail(outcome, signal: Signal):
        if not outcome:
            return None
        return {
            "status": outcome.outcome_status,
            "evaluation_method": outcome.evaluation_method,
            "entry_price": outcome.entry_reference_price,
            "resolution_price": outcome.resolution_price,
            "mfe_pct": outcome.max_favorable_excursion_pct,
            "mae_pct": outcome.max_adverse_excursion_pct,
            "return_pct": outcome.final_return_pct or 0,
            "bars": outcome.bars_to_resolution,
            "resolved_at": outcome.resolved_at,
            "notes": outcome.notes,
        }
