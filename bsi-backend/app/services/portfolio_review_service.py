from datetime import datetime, timedelta
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models.portfolio_profile import PortfolioProfile
from app.models.portfolio_position import PortfolioPosition
from app.models.portfolio_review import PortfolioReview
from app.models.portfolio_action_item import PortfolioActionItem
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.enums.portfolio import (
    ConcentrationStatus, RecommendationStatus, PositionStatus,
    PortfolioActionType
)
from app.enums.signal import SignalStatus, InterpretationStatus
from app.core.logging_utils import get_logger
from app.core.errors import NotFoundError, BusinessRuleError
from app.services.portfolio_service import PortfolioService

logger = get_logger("portfolio_review")

class PortfolioReviewService:
    @staticmethod
    def run_portfolio_review(db: Session, profile_id: int) -> PortfolioReview:
        profile = db.query(PortfolioProfile).filter(PortfolioProfile.id == profile_id).first()
        if not profile:
            raise NotFoundError("Profile not found", domain="portfolio")

        # 1. Get active positions
        active_positions = db.query(PortfolioPosition).filter(
            PortfolioPosition.status == PositionStatus.ACTIVE
        ).all()

        # 2. Calculate Diagnostic (Snapshot)
        # For Phase 10, current_price = entry_price (no real-time data yet)
        total_market_value_positions = sum(p.allocated_capital for p in active_positions)
        cash_balance = profile.initial_capital - total_market_value_positions
        total_market_value = profile.initial_capital # Assuming initial capital is the base

        # Drift & Concentration Analysis
        drift_analysis = {
            "domains": {},
            "positions": {}
        }
        
        domain_exposure = {}
        for pos in active_positions:
            domain = pos.signal.domain
            domain_exposure[domain] = domain_exposure.get(domain, 0.0) + pos.allocated_capital
            
            # Position drift (current weight vs max limit)
            current_weight = (pos.allocated_capital / total_market_value) * 100
            drift_analysis["positions"][pos.signal.asset] = {
                "current_weight": current_weight,
                "limit": profile.max_single_position_pct,
                "drift": max(0, current_weight - profile.max_single_position_pct)
            }

        concentration_warning = False
        for domain, exposure in domain_exposure.items():
            domain_weight = (exposure / total_market_value) * 100
            drift_analysis["domains"][domain] = {
                "current_weight": domain_weight,
                "limit": profile.max_domain_exposure_pct,
                "drift": max(0, domain_weight - profile.max_domain_exposure_pct)
            }
            if domain_weight > profile.max_domain_exposure_pct:
                concentration_warning = True

        concentration_status = ConcentrationStatus.WARNING if concentration_warning else ConcentrationStatus.HEALTHY
        # If any single position is critical...
        if any(d["drift"] > 5 for d in drift_analysis["positions"].values()):
            concentration_status = ConcentrationStatus.CRITICAL

        # 3. Evaluate Actions & Replacement
        action_items = []
        
        # A. Evaluate current positions (Hold/Reduce/Exit)
        for pos in active_positions:
            pos_drift = drift_analysis["positions"][pos.signal.asset]["drift"]
            if pos_drift > 0:
                action_items.append(PortfolioActionItem(
                    position_id=pos.id,
                    action_type=PortfolioActionType.REDUCE,
                    rationale=f"Posição excedeu o limite de {profile.max_single_position_pct}% (Atual: {drift_analysis['positions'][pos.signal.asset]['current_weight']:.1f}%)"
                ))
            else:
                # Check domain drift
                dom_drift = drift_analysis["domains"][pos.signal.domain]["drift"]
                if dom_drift > 0:
                    action_items.append(PortfolioActionItem(
                        position_id=pos.id,
                        action_type=PortfolioActionType.REDUCE,
                        rationale=f"Domínio {pos.signal.domain} excedeu o limite de {profile.max_domain_exposure_pct}%."
                    ) )
                else:
                    action_items.append(PortfolioActionItem(
                        position_id=pos.id,
                        action_type=PortfolioActionType.HOLD,
                        rationale="Posição aderente ao perfil e limites."
                    ))

        # B. Check for Superior Opportunities (REPLACE)
        # Get recent interpreted signals not in portfolio
        since = datetime.utcnow() - timedelta(hours=24)
        active_signal_ids = [p.signal_id for p in active_positions]
        new_signals = db.query(Signal).filter(
            Signal.status == SignalStatus.INTERPRETED,
            Signal.created_at >= since,
            ~Signal.id.in_(active_signal_ids)
        ).all()

        for sig in new_signals:
            interpretation = db.query(SignalInterpretation).filter(
                SignalInterpretation.signal_id == sig.id,
                SignalInterpretation.status == InterpretationStatus.SUCCESS
            ).first()
            
            if interpretation:
                score_data = PortfolioService.calculate_priority_score(interpretation, sig)
                new_score = score_data["final_score"]
                
                # Compare with weakest active position
                if active_positions:
                    # To compare, we need the scores of active positions at their time or current
                    # For simplicity, we re-calculate or fetch their interpretation score
                    weakest_pos = None
                    min_score = 101.0
                    
                    for pos in active_positions:
                        pos_itp = db.query(SignalInterpretation).filter(
                            SignalInterpretation.signal_id == pos.signal_id
                        ).first()
                        if pos_itp:
                            pos_score = PortfolioService.calculate_priority_score(pos_itp, pos.signal)["final_score"]
                            if pos_score < min_score:
                                min_score = pos_score
                                weakest_pos = pos
                    
                    # Replacement Heuristic: Score > weakest + 20
                    if weakest_pos and new_score > (min_score + 20):
                        action_items.append(PortfolioActionItem(
                            signal_id=sig.id,
                            position_id=weakest_pos.id,
                            action_type=PortfolioActionType.REPLACE,
                            priority_score_diff=new_score - min_score,
                            rationale=f"Oportunidade superior detectada ({sig.asset}). Score {new_score:.0f} vs {min_score:.0f} da posição atual mais fraca ({weakest_pos.signal.asset})."
                        ))

        # 4. Finalize Review
        review = PortfolioReview(
            profile_id=profile_id,
            total_market_value=total_market_value,
            cash_balance=cash_balance,
            drift_analysis_json=drift_analysis,
            concentration_status=concentration_status,
            status=RecommendationStatus.SUCCESS,
            summary="Análise de carteira concluída. Verifique as sugestões de manutenção."
        )
        
        db.add(review)
        db.flush()
        
        for item in action_items:
            item.review_id = review.id
            db.add(item)
            
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def run_review_for_default_profile(db: Session):
        profile = db.query(PortfolioProfile).first()
        if not profile:
            raise BusinessRuleError("Please configure a profile first", domain="portfolio")
        review = PortfolioReviewService.run_portfolio_review(db, profile.id)
        return PortfolioReviewService.serialize_review(review)

    @staticmethod
    def get_latest_review_data(db: Session):
        review = db.query(PortfolioReview).order_by(PortfolioReview.created_at.desc()).first()
        if not review:
            raise NotFoundError("No reviews found", domain="portfolio")
        return PortfolioReviewService.serialize_review(review)

    @staticmethod
    def acknowledge_action(db: Session, position_id: int):
        pos = db.query(PortfolioPosition).filter(PortfolioPosition.id == position_id).first()
        if not pos:
            raise NotFoundError("Position not found", domain="portfolio")
        pos.acknowledged_at = datetime.utcnow()
        db.commit()
        return {"status": "success"}

    @staticmethod
    def serialize_review(review: PortfolioReview):
        return {
            "id": review.id,
            "total_market_value": review.total_market_value,
            "cash_balance": review.cash_balance,
            "drift_analysis_json": review.drift_analysis_json,
            "concentration_status": review.concentration_status,
            "status": review.status,
            "summary": review.summary,
            "created_at": review.created_at,
            "actions": [
                {
                    "id": action.id,
                    "action_type": action.action_type,
                    "asset": action.position.signal.asset if action.position else action.signal.asset if action.signal else "Global",
                    "priority_score_diff": action.priority_score_diff,
                    "rationale": action.rationale,
                    "position_id": action.position_id,
                }
                for action in review.actions
            ],
        }
