from typing import Any, Dict
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.models.signal_outcome import SignalOutcome


class SystemService:
    def __init__(self, db: Session):
        self.db = db

    def get_status(self) -> Dict[str, Any]:
        database_ok = self._check_database()

        signal_count = self.db.query(Signal).count()
        interpretation_count = self.db.query(SignalInterpretation).count()
        outcome_count = self.db.query(SignalOutcome).count()

        crypto_count = self.db.query(Signal).filter(Signal.domain == "CRYPTO_SPOT").count()
        b3_count = self.db.query(Signal).filter(Signal.domain == "B3_EQUITIES").count()

        seeded_present = self.db.query(SignalOutcome).filter(SignalOutcome.data_quality == "SEEDED_DEMO").count() > 0
        real_present = self.db.query(SignalOutcome).filter(SignalOutcome.data_quality == "REAL_CAPTURED").count() > 0

        return {
            "app_name": settings.APP_NAME,
            "environment_mode": getattr(settings, "ENVIRONMENT_MODE", "UNKNOWN"),
            "database_ok": database_ok,
            "counts": {
                "signals": signal_count,
                "interpretations": interpretation_count,
                "outcomes": outcome_count,
                "by_domain": {
                    "CRYPTO_SPOT": crypto_count,
                    "B3_EQUITIES": b3_count,
                },
            },
            "indicators": {
                "seeded_data_present": seeded_present,
                "real_captured_present": real_present,
            },
        }

    def _check_database(self) -> bool:
        try:
            self.db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
