from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.interpretation_service import InterpretationService

from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response

DOMAIN = "interpretations"

router = APIRouter()

@router.post("/process-pending", status_code=status.HTTP_200_OK)
def process_pending_interpretations(db: Session = Depends(get_db)):
    """
    Busca todos os sinais com status STORED e dispara a interpretação via LLM.
    """
    data = InterpretationService(db).process_pending_signals_data()
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)

@router.post("/{signal_id}", status_code=status.HTTP_200_OK)
def interpret_single_signal(signal_id: int, db: Session = Depends(get_db)):
    """
    Dispara a interpretação para um sinal específico.
    """
    data = InterpretationService(db).interpret_signal_by_id(signal_id)
    res = StandardResponse.success_response(data=data, domain=DOMAIN)
    return to_compatible_response(res)
