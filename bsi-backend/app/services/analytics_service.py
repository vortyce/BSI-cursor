from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.models.signal_outcome import SignalOutcome
from typing import List, Dict, Any, Optional
import statistics

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_llm_impact_analysis(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Calcula o impacto incremental do LLM comparando grupos de sinais, respeitando o domínio (Fase 8 Fix).
        """
        results = []

        # Grupo 1: Baseline (Todos os Resolvidos do domínio)
        query_global = self.db.query(SignalOutcome).join(Signal, SignalOutcome.signal_id == Signal.id)\
            .filter(SignalOutcome.outcome_status != 'OPEN')
        if domain:
            query_global = query_global.filter(Signal.domain == domain)
        results.append(self._calculate_group_stats("Global (Baseline)", query_global.all()))

        # Grupo 2: Sinais com IA SUCCESS
        query_ia_success = self.db.query(SignalOutcome).join(Signal, SignalOutcome.signal_id == Signal.id)\
            .join(SignalInterpretation, SignalOutcome.signal_id == SignalInterpretation.signal_id)\
            .filter(SignalInterpretation.status == 'SUCCESS')\
            .filter(SignalOutcome.outcome_status != 'OPEN')
        if domain:
            query_ia_success = query_ia_success.filter(Signal.domain == domain)
        results.append(self._calculate_group_stats("IA Success Vetted", query_ia_success.all()))

        # Grupo 3: Sinais SEM IA ou IA FAILED
        ia_vetted_ids = self.db.query(SignalInterpretation.signal_id).filter(SignalInterpretation.status == 'SUCCESS').subquery()
        query_no_ia = self.db.query(SignalOutcome).join(Signal, SignalOutcome.signal_id == Signal.id)\
            .filter(SignalOutcome.signal_id.notin_(ia_vetted_ids))\
            .filter(SignalOutcome.outcome_status != 'OPEN')
        if domain:
            query_no_ia = query_no_ia.filter(Signal.domain == domain)
        results.append(self._calculate_group_stats("Raw (No IA Success)", query_no_ia.all()))

        # Grupo 4: IA HIGH CONFIDENCE
        query_ia_high = self.db.query(SignalOutcome).join(Signal, SignalOutcome.signal_id == Signal.id)\
            .join(SignalInterpretation, SignalOutcome.signal_id == SignalInterpretation.signal_id)\
            .filter(SignalInterpretation.confidence_level == 'HIGH')\
            .filter(SignalOutcome.outcome_status != 'OPEN')
        if domain:
            query_ia_high = query_ia_high.filter(Signal.domain == domain)
        results.append(self._calculate_group_stats("IA High Confidence", query_ia_high.all()))

        return results

    def _calculate_group_stats(self, name: str, outcomes: List[SignalOutcome]) -> Dict[str, Any]:
        n = len(outcomes)
        if n == 0:
            return {
                "group": name,
                "n": 0,
                "win_rate": 0,
                "avg_return_pct": 0,
                "median_return_pct": 0,
                "resolved_rate": 0
            }

        wins = [o for o in outcomes if o.outcome_status == 'WIN']
        returns = [o.final_return_pct or 0 for o in outcomes]
        
        return {
            "group": name,
            "n": n,
            "win_rate": (len(wins) / n * 100),
            "avg_return_pct": sum(returns) / n,
            "median_return_pct": statistics.median(returns) if returns else 0,
            "resolved_rate": 100.0
        }
