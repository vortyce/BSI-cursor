from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.outcome_service import OutcomeService
from typing import Dict, Any

from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response

DOMAIN = "outcomes"

router = APIRouter()

@router.get("/summary")
def get_summary(quality: str = None, domain: str = None, db: Session = Depends(get_db)):
    service = OutcomeService(db)
    data = service.get_performance_summary(quality=quality, domain=domain)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/breakdown/{dimension}")
def get_breakdown(dimension: str, quality: str = None, domain: str = None, db: Session = Depends(get_db)):
    service = OutcomeService(db)
    data = service.get_breakdown_by_dimension(dimension, quality=quality, domain=domain)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.post("/webhook-callback/{signal_id}")
def register_outcome_webhook(signal_id: int, data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Endpoint oficial para recepção do desfecho (Outcome) via TradingView.
    """
    service = OutcomeService(db)
    data_out = service.register_outcome_via_webhook(signal_id, data)
    res = StandardResponse.success_response(data=data_out, domain=DOMAIN)
    return to_compatible_response(res)
