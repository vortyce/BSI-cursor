from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.system_service import SystemService

from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response

DOMAIN = "system"

router = APIRouter()

@router.get("/status")
def get_system_status(db: Session = Depends(get_db)):
    """
    Endpoint de governança e saúde operacional (Fase 7/8).
    """
    data = SystemService(db).get_status()
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)
