from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.portfolio_decision import PortfolioDecision
from app.models.portfolio_action_item import PortfolioActionItem
from app.models.portfolio_position import PortfolioPosition
from app.models.signal import Signal
from app.enums.decision import UserChoice, SimulatedExecutionStatus
from app.enums.portfolio import PositionStatus, PortfolioActionType
from app.core.logging_utils import get_logger
from app.core.errors import NotFoundError

logger = get_logger("decision")

class DecisionService:
    ACTIONABLE_SIMULATION_TYPES = {
        PortfolioActionType.REPLACE,
        PortfolioActionType.EXIT,
        PortfolioActionType.REDUCE,
    }

    @staticmethod
    def record_user_choice(db: Session, action_item_id: int, choice: UserChoice, notes: Optional[str] = None) -> PortfolioDecision:
        try:
            action_item = db.query(PortfolioActionItem).filter(PortfolioActionItem.id == action_item_id).first()
            if not action_item:
                raise NotFoundError("Action item not found", domain="portfolio")

            decision = PortfolioDecision(
                action_item_id=action_item_id,
                user_choice=choice,
                user_notes=notes,
                decision_timestamp=datetime.utcnow()
            )
            db.add(decision)
            db.flush()

            if choice == UserChoice.ACCEPTED and action_item.action_type in DecisionService.ACTIONABLE_SIMULATION_TYPES:
                DecisionService.apply_simulated_impact(db, decision, action_item)
            elif choice == UserChoice.ACCEPTED:
                decision.simulated_execution_status = SimulatedExecutionStatus.NONE
                decision.impact_snapshot_json = {
                    "type": action_item.action_type,
                    "note": "No simulated mutation is defined for this action type."
                }
            
            db.commit()
            db.refresh(decision)
            return decision
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def record_user_choice_data(db: Session, action_item_id: int, choice: UserChoice, notes: Optional[str] = None):
        decision = DecisionService.record_user_choice(db, action_item_id, choice, notes)
        return DecisionService.serialize_decision(decision)

    @staticmethod
    def apply_simulated_impact(db: Session, decision: PortfolioDecision, action: PortfolioActionItem):
        """
        [MVP SIMULATION POLICY]
        This method implements provisional heuristics to reflect user intent on the simulated portfolio.
        These rules are audit-only and do not represent a definitive financial policy or real execution.
        """
        impact = {"before": {}, "after": {}, "type": action.action_type}
        
        try:
            if action.action_type == PortfolioActionType.REPLACE:
                # HEURISTIC: Close old and open new using trigger price as proxy
                if action.position_id:
                    old_pos = db.query(PortfolioPosition).filter(PortfolioPosition.id == action.position_id).first()
                    if old_pos:
                        impact["before"]["old_position"] = {"id": old_pos.id, "asset": old_pos.signal.asset}
                        old_pos.status = PositionStatus.CLOSED
                        old_pos.exit_price = old_pos.signal.trigger_price 
                        impact["after"]["old_position"] = {"status": "CLOSED"}
                
                if action.signal_id:
                    sig = db.query(Signal).filter(Signal.id == action.signal_id).first()
                    if sig:
                        new_pos = PortfolioPosition(
                            signal_id=sig.id,
                            entry_price=sig.trigger_price,
                            # HEURISTIC: Fixed allocation based on profile max single position %
                            allocated_capital=action.review.profile.initial_capital * (action.review.profile.max_single_position_pct / 100),
                            status=PositionStatus.ACTIVE,
                            entry_rationale=f"Simulated Replace Decision based on Review {action.review_id}"
                        )
                        db.add(new_pos)
                        db.flush()
                        impact["after"]["new_position"] = {"id": new_pos.id, "asset": sig.asset}

            elif action.action_type == PortfolioActionType.EXIT:
                # HEURISTIC: Close position immediately at trigger price
                if action.position_id:
                    pos = db.query(PortfolioPosition).filter(PortfolioPosition.id == action.position_id).first()
                    if pos:
                        impact["before"]["position"] = {"id": pos.id, "asset": pos.signal.asset}
                        pos.status = PositionStatus.CLOSED
                        pos.exit_price = pos.signal.trigger_price
                        impact["after"]["position"] = {"status": "CLOSED"}

            elif action.action_type == PortfolioActionType.REDUCE:
                # HEURISTIC: Fixed 50% capital reduction for intent simulation
                if action.position_id:
                    pos = db.query(PortfolioPosition).filter(PortfolioPosition.id == action.position_id).first()
                    if pos:
                        impact["before"]["capital"] = pos.allocated_capital
                        pos.allocated_capital = pos.allocated_capital * 0.5
                        pos.status = PositionStatus.REDUCED
                        impact["after"]["capital"] = pos.allocated_capital
            if impact["after"]:
                decision.simulated_execution_status = SimulatedExecutionStatus.APPLIED
                decision.impact_snapshot_json = impact
            else:
                decision.simulated_execution_status = SimulatedExecutionStatus.NONE
                decision.impact_snapshot_json = {
                    "type": action.action_type,
                    "note": "No simulated mutation was applied."
                }

        except Exception as e:
            # Graceful failure for MVP simulation errors
            decision.simulated_execution_status = SimulatedExecutionStatus.FAILED
            decision.impact_snapshot_json = {"error": str(e), "note": "Simulation heuristic failed to process mutation."}

    @staticmethod
    def get_decision_history(db: Session, limit: int = 50) -> List[PortfolioDecision]:
        return db.query(PortfolioDecision).order_by(PortfolioDecision.decision_timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_pending_recommendations(db: Session):
        since = datetime.utcnow() - timedelta(hours=48)
        
        final_decided_ids = db.query(PortfolioDecision.action_item_id).filter(
            PortfolioDecision.user_choice.in_([
                UserChoice.ACCEPTED,
                UserChoice.REJECTED,
                UserChoice.EXPIRED,
            ])
        ).all()
        final_decided_ids = [r[0] for r in final_decided_ids]

        deferred_ids = db.query(PortfolioDecision.action_item_id).filter(
            PortfolioDecision.user_choice == UserChoice.DEFERRED
        ).all()
        deferred_ids = [r[0] for r in deferred_ids]
        
        return db.query(PortfolioActionItem).filter(
            PortfolioActionItem.action_type.notin_([
                PortfolioActionType.HOLD,
                PortfolioActionType.NO_ACTION,
            ]),
            ~PortfolioActionItem.id.in_(final_decided_ids),
            or_(
                PortfolioActionItem.created_at >= since,
                PortfolioActionItem.id.in_(deferred_ids),
            )
        ).all()

    @staticmethod
    def get_pending_recommendations_data(db: Session):
        return [
            DecisionService.serialize_action_item(item)
            for item in DecisionService.get_pending_recommendations(db)
        ]

    @staticmethod
    def get_decision_history_data(db: Session, limit: int = 50):
        return [
            DecisionService.serialize_decision(decision)
            for decision in DecisionService.get_decision_history(db, limit=limit)
        ]

    @staticmethod
    def serialize_action_item(item: PortfolioActionItem):
        return {
            "id": item.id,
            "action_type": item.action_type,
            "asset": item.position.signal.asset if item.position else item.signal.asset if item.signal else "Global",
            "rationale": item.rationale,
            "priority_score_diff": item.priority_score_diff,
            "created_at": item.created_at,
        }

    @staticmethod
    def serialize_decision(decision: PortfolioDecision):
        action_item = decision.action_item
        return {
            "id": decision.id,
            "action_type": action_item.action_type,
            "asset": action_item.position.signal.asset if action_item.position else action_item.signal.asset if action_item.signal else "Global",
            "user_choice": decision.user_choice,
            "decision_timestamp": decision.decision_timestamp,
            "simulated_execution_status": decision.simulated_execution_status,
            "impact": decision.impact_snapshot_json,
            "notes": decision.user_notes,
        }
