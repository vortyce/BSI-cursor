from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.portfolio_service import PortfolioService
from app.services.portfolio_review_service import PortfolioReviewService
from app.services.decision_service import DecisionService
from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response
from app.schemas.portfolio import ProfileDTO, DecisionRequestDTO

DOMAIN = "portfolio"


router = APIRouter()

@router.post("/profile")
def create_or_update_profile(data: ProfileDTO, db: Session = Depends(get_db)):
    profile = PortfolioService.save_profile(db, data.model_dump())
    res = StandardResponse.success_response(data=profile, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = PortfolioService.get_profile_data(db)
    res = StandardResponse.success_response(data=profile, domain=DOMAIN)
    return to_compatible_response(res)

@router.post("/recommendation/run")
def run_recommendation(db: Session = Depends(get_db)):
    data = PortfolioService.run_recommendation_for_default_profile(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/recommendation/latest")
def get_latest_recommendation(db: Session = Depends(get_db)):
    data = PortfolioService.get_latest_recommendation_data(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/positions")
def get_positions(db: Session = Depends(get_db)):
    data = PortfolioService.get_active_positions_data(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.post("/review/run")
def run_review(db: Session = Depends(get_db)):
    data = PortfolioReviewService.run_review_for_default_profile(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/review/latest")
def get_latest_review(db: Session = Depends(get_db)):
    data = PortfolioReviewService.get_latest_review_data(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.post("/positions/{id}/acknowledge")
def acknowledge_position(id: int, db: Session = Depends(get_db)):
    data = PortfolioReviewService.acknowledge_action(db, id)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/recommendations/pending")
def get_pending_recommendations(db: Session = Depends(get_db)):
    data = DecisionService.get_pending_recommendations_data(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.post("/decisions")
def record_decision(req: DecisionRequestDTO, db: Session = Depends(get_db)):
    data = DecisionService.record_user_choice_data(db, req.action_item_id, req.choice, req.notes)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/decisions/history")
def get_decision_history(db: Session = Depends(get_db)):
    data = DecisionService.get_decision_history_data(db)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)
