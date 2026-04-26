from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.webhook_ingestion_service import WebhookIngestionService
from app.schemas.webhook import TradingViewWebhook
from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response
from app.core.logging_utils import get_logger

DOMAIN = "webhooks"
logger = get_logger(DOMAIN)

router = APIRouter()

@router.post("/tradingview")
async def tradingview_webhook(payload: TradingViewWebhook, db: Session = Depends(get_db)):
    service = WebhookIngestionService(db)
    data = service.process_webhook(payload)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/signals")
def list_signals(domain: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retorna a lista de sinais com suporte a filtro de domínio (Fase 8).
    """
    data = WebhookIngestionService(db).list_signals(domain=domain)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.get("/signals/{signal_id}/full")
def get_signal_full_detail(signal_id: int, db: Session = Depends(get_db)):
    """
    Retorna o detalhe completo agregado.
    """
    data = WebhookIngestionService(db).get_signal_full_detail(signal_id)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)
