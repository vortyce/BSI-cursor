from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.analytics_service import AnalyticsService
from typing import List, Dict, Any, Optional
from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response

DOMAIN = "analytics"

router = APIRouter()

@router.get("/llm-impact")
def get_llm_impact(domain: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retorna análise detalhada do impacto do LLM na performance dos sinais, com suporte a filtro de domínio.
    """
    service = AnalyticsService(db)
    data = service.get_llm_impact_analysis(domain=domain)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)
