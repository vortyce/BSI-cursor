from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.models.signal_outcome import SignalOutcome
from typing import List, Dict, Any
import statistics
from app.core.errors import NotFoundError, ValidationError

class OutcomeService:
    def __init__(self, db: Session):
        self.db = db

    def get_performance_summary(self, quality: str = None, domain: str = None) -> Dict[str, Any]:
        """
        Métricas refinadas com suporte a filtragem por Domínio (Fase 8).
        """
        query_outcomes = self.db.query(SignalOutcome).join(Signal, SignalOutcome.signal_id == Signal.id)
        query_signals = self.db.query(Signal)
        
        if quality:
            query_outcomes = query_outcomes.filter(SignalOutcome.data_quality == quality)
            query_signals = query_signals.join(SignalOutcome, Signal.id == SignalOutcome.signal_id)\
                                         .filter(SignalOutcome.data_quality == quality)
        
        if domain:
            query_outcomes = query_outcomes.filter(Signal.domain == domain)
            query_signals = query_signals.filter(Signal.domain == domain)

        all_outcomes = query_outcomes.all()
        resolved = [o for o in all_outcomes if o.outcome_status != 'OPEN']
        total_signals = query_signals.count()
        n_resolved = len(resolved)
        
        if total_signals == 0:
            return {"total_signals": 0, "n_resolved": 0, "status": "No data found"}

        # Taxas de Interpretação
        interpreted_success_count = query_signals.join(SignalInterpretation, Signal.id == SignalInterpretation.signal_id)\
            .filter(SignalInterpretation.status == 'SUCCESS').count()
        
        interpreted_failed_count = query_signals.join(SignalInterpretation, Signal.id == SignalInterpretation.signal_id)\
            .filter(SignalInterpretation.status == 'FAILED').count()
        
        no_interp_count = total_signals - (interpreted_success_count + interpreted_failed_count)

        # Métricas de Volume
        resolved_rate = (n_resolved / total_signals * 100) if total_signals > 0 else 0
        open_rate = 100 - resolved_rate

        # Métricas de Performance
        wins = [o for o in resolved if o.outcome_status == 'WIN']
        returns = [o.final_return_pct or 0 for o in resolved]

        # IA Success Sample
        ia_success_resolved = self.db.query(SignalOutcome)\
            .join(Signal, SignalOutcome.signal_id == Signal.id)\
            .join(SignalInterpretation, SignalOutcome.signal_id == SignalInterpretation.signal_id)\
            .filter(SignalInterpretation.status == 'SUCCESS')\
            .filter(SignalOutcome.outcome_status != 'OPEN')
        
        if quality:
            ia_success_resolved = ia_success_resolved.filter(SignalOutcome.data_quality == quality)
        if domain:
            ia_success_resolved = ia_success_resolved.filter(Signal.domain == domain)
            
        ia_success_resolved = ia_success_resolved.all()
        n_ia_success = len(ia_success_resolved)
        wr_ia_success = (len([o for o in ia_success_resolved if o.outcome_status == 'WIN']) / n_ia_success * 100) if n_ia_success > 0 else 0

        return {
            "total_signals": total_signals,
            "n_resolved": n_resolved,
            "resolved_rate": resolved_rate,
            "open_rate": open_rate,
            "interpreted_success_rate": (interpreted_success_count / total_signals * 100),
            "interpreted_failed_rate": (interpreted_failed_count / total_signals * 100),
            "no_interpretation_rate": (no_interp_count / total_signals * 100),
            "win_rate_global": (len(wins) / n_resolved * 100) if n_resolved > 0 else 0,
            "win_rate_ia_success": wr_ia_success,
            "n_ia_success": n_ia_success,
            "avg_return_pct": sum(returns) / n_resolved if n_resolved > 0 else 0,
            "median_return_pct": statistics.median(returns) if resolved else 0,
            "data_quality_label": quality or "ALL",
            "domain": domain or "ALL"
        }

    def get_breakdown_by_dimension(self, dimension: str, quality: str = None, domain: str = None) -> List[Dict[str, Any]]:
        """
        Breakdown com suporte a filtragem por Domínio.
        """
        if dimension not in ["confidence_level", "regime", "context_alignment", "profile_fit", "primary_thesis"]:
            raise ValidationError("Dimensão inválida", domain="outcomes", details={"dimension": dimension})

        base_query = self.db.query(
            getattr(SignalInterpretation, dimension).label("label"),
            SignalOutcome.final_return_pct,
            SignalOutcome.outcome_status
        ).join(SignalInterpretation, SignalOutcome.signal_id == SignalInterpretation.signal_id)\
         .join(Signal, SignalOutcome.signal_id == Signal.id)
        
        if quality:
            base_query = base_query.filter(SignalOutcome.data_quality == quality)
        if domain:
            base_query = base_query.filter(Signal.domain == domain)
            
        rows = base_query.filter(SignalOutcome.outcome_status != 'OPEN').all()
        
        groups = {}
        for row in rows:
            label = row.label or "N/A"
            if label not in groups:
                groups[label] = {"returns": [], "wins": 0}
            groups[label]["returns"].append(row.final_return_pct or 0)
            if row.outcome_status == 'WIN':
                groups[label]["wins"] += 1
                
        results = []
        for label, data in groups.items():
            n = len(data["returns"])
            results.append({
                "label": label,
                "n": n,
                "win_rate": (data["wins"] / n * 100) if n > 0 else 0,
                "avg_return_pct": sum(data["returns"]) / n if n > 0 else 0,
                "median_return_pct": statistics.median(data["returns"]) if n > 0 else 0,
                "sample_too_small": n < 5
            })
            
        return sorted(results, key=lambda x: x["n"], reverse=True)

    def register_outcome_via_webhook(self, signal_id: int, data: Dict[str, Any]):
        signal = self.db.query(Signal).filter(Signal.id == signal_id).first()
        if not signal:
            raise NotFoundError("Signal not found", domain="outcomes")

        outcome = self.db.query(SignalOutcome).filter(SignalOutcome.signal_id == signal_id).first()
        if not outcome:
            outcome = SignalOutcome(
                signal_id=signal_id,
                entry_reference_price=signal.trigger_price,
                outcome_status=data.get("status", "INCONCLUSIVE"),
                evaluation_method="TRADINGVIEW_FOLLOWUP",
            )
            self.db.add(outcome)

        outcome.outcome_status = data.get("status", "INCONCLUSIVE")
        outcome.evaluation_method = "TRADINGVIEW_FOLLOWUP"
        outcome.resolution_price, outcome.final_return_pct = data.get("resolution_price"), data.get("return_pct", 0)
        outcome.bars_to_resolution = data.get("bars", 0)
        self.db.commit()
        return outcome
