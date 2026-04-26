from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.portfolio_profile import PortfolioProfile
from app.models.portfolio_position import PortfolioPosition
from app.models.allocation_recommendation import AllocationRecommendation
from app.models.allocation_item import AllocationItem
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.models.signal_outcome import SignalOutcome
from app.enums.portfolio import (
    AllocationStatus, RecommendationStatus, RiskProfile, 
    PositionStatus
)
from app.enums.signal import (
    ThesisCategory, InterpretationStatus, SignalStatus,
    DataSourceQuality
)

from app.core.logging_utils import get_logger
from app.core.errors import NotFoundError, BusinessRuleError

logger = get_logger("portfolio")

class PortfolioService:
    RISK_ALLOCATION_POLICY = {
        RiskProfile.CONSERVATIVE: {
            "crypto_cap_pct": 10.0,
            "b3_min_pct": 80.0,
            "cash_reserve_cap_pct": 20.0,
            "cap_rationale": "Crypto allocation capped due to conservative risk profile.",
        },
        RiskProfile.MODERATE: {
            "crypto_cap_pct": 20.0,
            "b3_min_pct": 60.0,
            "cash_reserve_cap_pct": 20.0,
            "cap_rationale": "Crypto allocation capped due to moderate risk profile.",
        },
        RiskProfile.AGGRESSIVE: {
            "crypto_cap_pct": 35.0,
            "b3_min_pct": 40.0,
            "cash_reserve_cap_pct": None,
            "cap_rationale": "Crypto allocation capped due to aggressive risk profile.",
        },
    }

    @staticmethod
    def save_profile(db: Session, profile_data: dict) -> PortfolioProfile:
        """
        Explicit Single Profile Mode (MVP Fase 9):
        Garante que exista apenas um perfil global. Se já existir, atualiza.
        """
        try:
            profile = db.query(PortfolioProfile).order_by(PortfolioProfile.id.asc()).first()
            if profile:
                logger.info("save_profile", "Updating existing portfolio profile")
                for key, value in profile_data.items():
                    setattr(profile, key, value)
            else:
                logger.info("save_profile", "Creating new portfolio profile")
                profile = PortfolioProfile(**profile_data)
                db.add(profile)
            
            db.commit()
            db.refresh(profile)
            logger.info("save_profile", "Portfolio profile saved successfully")
            return profile
        except Exception as e:
            db.rollback()
            logger.error("save_profile", f"Error saving portfolio profile: {str(e)}")
            raise e

    @staticmethod
    def get_profile(db: Session, profile_id: int) -> Optional[PortfolioProfile]:
        # Em modo de Single Profile, retorna o primeiro (e único) registro
        if profile_id is None:
            return db.query(PortfolioProfile).order_by(PortfolioProfile.id.asc()).first()
        return db.query(PortfolioProfile).filter(PortfolioProfile.id == profile_id).first()

    @staticmethod
    def get_profile_data(db: Session):
        profile = PortfolioService.get_profile(db, None)
        if not profile:
            raise NotFoundError("Profile not found", domain="portfolio")
        return profile

    @staticmethod
    def run_recommendation_for_default_profile(db: Session):
        profile = PortfolioService.get_profile(db, None)
        if not profile:
            raise BusinessRuleError("Please configure a profile first", domain="portfolio")
        recommendation = PortfolioService.run_allocation_engine(db, profile.id)
        return PortfolioService.serialize_recommendation(recommendation)

    @staticmethod
    def get_latest_recommendation_data(db: Session):
        recommendation = db.query(AllocationRecommendation).order_by(AllocationRecommendation.created_at.desc()).first()
        if not recommendation:
            raise NotFoundError("No recommendations found", domain="portfolio")
        return PortfolioService.serialize_recommendation(recommendation)

    @staticmethod
    def get_active_positions_data(db: Session):
        positions = db.query(PortfolioPosition).filter(PortfolioPosition.status == PositionStatus.ACTIVE).all()
        return [PortfolioService.serialize_position(position) for position in positions]

    @staticmethod
    def serialize_recommendation(recommendation: AllocationRecommendation):
        return {
            "id": recommendation.id,
            "total_capital": recommendation.total_capital,
            "cash_reserve": recommendation.cash_reserve,
            "available_capital": recommendation.available_capital,
            "allocated_capital": recommendation.allocated_capital,
            "unallocated_capital": recommendation.unallocated_capital,
            "macro_allocation_json": recommendation.macro_allocation_json,
            "rationale_summary": recommendation.rationale_summary,
            "status": recommendation.status,
            "created_at": recommendation.created_at,
            "items": [
                {
                    "id": item.id,
                    "signal_id": item.signal_id,
                    "asset": item.signal.asset,
                    "domain": item.signal.domain,
                    "direction": item.signal.signal_direction,
                    "suggested_allocation_pct": item.suggested_allocation_pct,
                    "suggested_allocation_amount": item.suggested_allocation_amount,
                    "status": item.status,
                    "priority_score": item.priority_score,
                    "priority_score_components": item.priority_score_components,
                    "rationale": item.rationale,
                }
                for item in recommendation.items
            ],
        }

    @staticmethod
    def serialize_position(position: PortfolioPosition):
        return {
            "id": position.id,
            "signal_id": position.signal_id,
            "asset": position.signal.asset,
            "domain": position.signal.domain,
            "entry_price": position.entry_price,
            "allocated_capital": position.allocated_capital,
            "status": position.status,
            "entry_rationale": position.entry_rationale,
            "acknowledged_at": position.acknowledged_at,
            "created_at": position.created_at,
        }

    @staticmethod
    def calculate_priority_score(interpretation: SignalInterpretation, signal: Signal) -> dict:
        # Confidence (0-100)
        confidence = interpretation.confidence_score or 0
        
        # Alignment (0-100)
        alignment_map = {
            "ALIGNED": 100,
            "PARTIAL": 50,
            "CONFLICTING": 0
        }
        alignment_score = alignment_map.get(interpretation.context_alignment, 0)
        
        # Thesis (0-100)
        thesis_high = [ThesisCategory.TREND_ALIGNED, ThesisCategory.BREAKOUT_CONTEXT, ThesisCategory.CONSERVATIVE_FIT]
        thesis_medium = [ThesisCategory.VOLATILITY_WARNING, ThesisCategory.AGGRESSIVE_ONLY]
        
        if interpretation.primary_thesis in thesis_high:
            thesis_score = 100
        elif interpretation.primary_thesis in thesis_medium:
            thesis_score = 50
        else:
            thesis_score = 0
            
        # Data Quality (Heurística Simplificada - MVP Placeholder)
        # TODO Fase 10+: Integrar métricas reais de liquidez, slippage e latência.
        # Atualmente assume 100 para manter a transparência de que é um componente estático.
        dq_score = 100 
        
        # Final Score
        final_score = (confidence * 0.4) + (alignment_score * 0.3) + (thesis_score * 0.2) + (dq_score * 0.1)
        
        return {
            "final_score": final_score,
            "components": {
                "confidence": confidence,
                "alignment": alignment_score,
                "thesis": thesis_score,
                "data_quality": dq_score
            }
        }

    @staticmethod
    def get_risk_allocation_policy(risk_profile: RiskProfile) -> dict:
        return PortfolioService.RISK_ALLOCATION_POLICY.get(
            risk_profile,
            PortfolioService.RISK_ALLOCATION_POLICY[RiskProfile.MODERATE],
        )

    @staticmethod
    def run_allocation_engine(db: Session, profile_id: int) -> AllocationRecommendation:
        logger.info("run_allocation_engine", f"Starting allocation engine for profile_id={profile_id}")
        try:
            profile = db.query(PortfolioProfile).filter(PortfolioProfile.id == profile_id).first()
            if not profile:
                logger.error("run_allocation_engine", "Profile not found")
                raise ValueError("Profile not found")

            # 1. Get interpreted signals (active/recent - last 24h)
            since = datetime.utcnow() - timedelta(hours=24)
            signals = db.query(Signal).filter(
                Signal.status == SignalStatus.INTERPRETED,
                Signal.created_at >= since
            ).all()

            # 2. Get interpretations and calculate scores
            candidates = []
            for signal in signals:
                interpretation = db.query(SignalInterpretation).filter(
                    SignalInterpretation.signal_id == signal.id,
                    SignalInterpretation.status == InterpretationStatus.SUCCESS
                ).order_by(SignalInterpretation.created_at.desc()).first()
                
                if interpretation:
                    score_data = PortfolioService.calculate_priority_score(interpretation, signal)
                    candidates.append({
                        "signal": signal,
                        "interpretation": interpretation,
                        "score": score_data["final_score"],
                        "components": score_data["components"]
                    })

            # Sort by score descending
            candidates.sort(key=lambda x: x["score"], reverse=True)

            # 3. Allocation logic
            total_capital = profile.initial_capital
            allocation_policy = PortfolioService.get_risk_allocation_policy(profile.risk_profile)
            cash_reserve_pct = profile.keep_cash_reserve_pct
            if allocation_policy["cash_reserve_cap_pct"] is not None:
                cash_reserve_pct = min(cash_reserve_pct, allocation_policy["cash_reserve_cap_pct"])

            cash_reserve = total_capital * (cash_reserve_pct / 100)
            available_capital = total_capital - cash_reserve
            
            allocated_capital = 0.0
            domain_exposure = {domain: 0.0 for domain in profile.allowed_domains}
            
            items = []
            macro_allocation = {domain: 0.0 for domain in profile.allowed_domains}

            for candidate in candidates:
                sig = candidate["signal"]
                itp = candidate["interpretation"]
                score = candidate["score"]
                
                # Check domain
                if sig.domain not in profile.allowed_domains:
                    items.append(AllocationItem(
                        signal_id=sig.id,
                        suggested_allocation_pct=0,
                        suggested_allocation_amount=0,
                        status=AllocationStatus.REJECTED,
                        priority_score=score,
                        priority_score_components=candidate["components"],
                        rationale=f"Domain {sig.domain} not allowed in profile."
                    ))
                    continue

                # Check Risk Profile compatibility
                if itp.primary_thesis == ThesisCategory.AGGRESSIVE_ONLY and profile.risk_profile != RiskProfile.AGGRESSIVE:
                    items.append(AllocationItem(
                        signal_id=sig.id,
                        suggested_allocation_pct=0,
                        suggested_allocation_amount=0,
                        status=AllocationStatus.OUT_OF_PROFILE,
                        priority_score=score,
                        priority_score_components=candidate["components"],
                        rationale="Opportunity requires Aggressive profile."
                    ))
                    continue

                # Check Confidence Threshold
                if score < 40:
                    items.append(AllocationItem(
                        signal_id=sig.id,
                        suggested_allocation_pct=0,
                        suggested_allocation_amount=0,
                        status=AllocationStatus.LOW_PRIORITY,
                        priority_score=score,
                        priority_score_components=candidate["components"],
                        rationale="Heuristic score below minimum threshold."
                    ))
                    continue

                # Calculate proposed amount
                max_pos = total_capital * (profile.max_single_position_pct / 100)
                profile_domain_cap = total_capital * (profile.max_domain_exposure_pct / 100)
                policy_domain_cap = profile_domain_cap
                cap_rationale = None

                if sig.domain == "CRYPTO_SPOT":
                    policy_domain_cap = total_capital * (allocation_policy["crypto_cap_pct"] / 100)
                    cap_rationale = allocation_policy["cap_rationale"]
                elif sig.domain == "B3_EQUITIES":
                    b3_floor = total_capital * (allocation_policy["b3_min_pct"] / 100)
                    policy_domain_cap = max(profile_domain_cap, b3_floor)

                domain_cap = max(profile_domain_cap, policy_domain_cap) if sig.domain == "B3_EQUITIES" else min(profile_domain_cap, policy_domain_cap)
                remaining_domain_cap = domain_cap - domain_exposure.get(sig.domain, 0)
                remaining_total_cap = available_capital - allocated_capital

                b3_floor_remaining = 0.0
                if "B3_EQUITIES" in profile.allowed_domains and sig.domain != "B3_EQUITIES":
                    b3_floor = total_capital * (allocation_policy["b3_min_pct"] / 100)
                    b3_floor_remaining = max(0.0, b3_floor - domain_exposure.get("B3_EQUITIES", 0))
                    remaining_total_cap = max(0.0, remaining_total_cap - b3_floor_remaining)
                
                suggested_amount = min(max_pos, remaining_domain_cap, remaining_total_cap)
                uncapped_amount = min(max_pos, profile_domain_cap - domain_exposure.get(sig.domain, 0), available_capital - allocated_capital)

                if sig.domain == "B3_EQUITIES":
                    b3_floor = total_capital * (allocation_policy["b3_min_pct"] / 100)
                    b3_floor_remaining = max(0.0, b3_floor - domain_exposure.get("B3_EQUITIES", 0))
                    if b3_floor_remaining > suggested_amount:
                        suggested_amount = min(
                            b3_floor_remaining,
                            remaining_domain_cap,
                            available_capital - allocated_capital,
                        )
                
                if suggested_amount <= 0:
                    if sig.domain == "CRYPTO_SPOT" and remaining_domain_cap <= 0 and cap_rationale:
                        reason = cap_rationale
                    elif b3_floor_remaining > 0 and sig.domain == "CRYPTO_SPOT" and cap_rationale:
                        reason = cap_rationale
                    elif b3_floor_remaining > 0 and sig.domain != "B3_EQUITIES":
                        reason = "Capital reserved for B3 minimum allocation under risk profile policy."
                    else:
                        reason = "Domain exposure limit reached." if remaining_domain_cap <= 0 else "Total available capital reached."
                    items.append(AllocationItem(
                        signal_id=sig.id,
                        suggested_allocation_pct=0,
                        suggested_allocation_amount=0,
                        status=AllocationStatus.CAPITAL_CONSTRAINED,
                        priority_score=score,
                        priority_score_components=candidate["components"],
                        rationale=reason
                    ))
                    continue

                # Recommended
                allocated_capital += suggested_amount
                domain_exposure[sig.domain] = domain_exposure.get(sig.domain, 0) + suggested_amount
                macro_allocation[sig.domain] = macro_allocation.get(sig.domain, 0) + suggested_amount

                rationale = f"Opportunity aligned with {profile.risk_profile.value} profile and high score."
                if sig.domain == "CRYPTO_SPOT" and cap_rationale and suggested_amount < uncapped_amount:
                    rationale = f"{rationale} {cap_rationale}"
                elif sig.domain == "B3_EQUITIES" and b3_floor_remaining > max_pos:
                    rationale = f"{rationale} B3 allocation prioritized to satisfy risk profile minimum."
                
                items.append(AllocationItem(
                    signal_id=sig.id,
                    suggested_allocation_pct=(suggested_amount / total_capital) * 100,
                    suggested_allocation_amount=suggested_amount,
                    status=AllocationStatus.RECOMMENDED,
                    priority_score=score,
                    priority_score_components=candidate["components"],
                    rationale=rationale
                ))

            # Finalize recommendation
            rec_status = RecommendationStatus.SUCCESS if allocated_capital > 0 else RecommendationStatus.NO_ACTION
            
            recommendation = AllocationRecommendation(
                profile_id=profile_id,
                total_capital=total_capital,
                cash_reserve=cash_reserve,
                available_capital=available_capital,
                allocated_capital=allocated_capital,
                unallocated_capital=available_capital - allocated_capital,
                macro_allocation_json=macro_allocation,
                rationale_summary="No opportunities met the threshold." if rec_status == RecommendationStatus.NO_ACTION else "Capital distributed based on priority and constraints.",
                status=rec_status,
                items=items
            )
            
            db.add(recommendation)
            db.commit()
            db.refresh(recommendation)
            logger.info("run_allocation_engine", f"Allocation engine finished with status={rec_status}")
            return recommendation
        except Exception as e:
            db.rollback()
            logger.error("run_allocation_engine", f"Error in allocation engine: {str(e)}")
            raise e
