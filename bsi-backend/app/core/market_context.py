from datetime import datetime, time
import pytz
from app.enums.signal import MarketSession, SignalDomain

def get_market_session(timestamp: datetime, domain: str) -> MarketSession:
    """
    Deriva a sessão de mercado baseada no timestamp e domínio.
    Para B3, assume-se Horário de Brasília (UTC-3).
    """
    if domain != SignalDomain.B3_EQUITIES:
        return MarketSession.REGULAR_SESSION # Crypto is 24/7

    # Converter para Horário de Brasília (BRT)
    # Nota: Em ambiente real usaríamos pytz ou zoneinfo com feriados.
    # Para MVP, usamos um offset fixo de -3.
    br_hour = (timestamp.hour - 3) % 24
    br_time = time(br_hour, timestamp.minute)

    # Regras Simples B3
    if time(9, 0) <= br_time < time(10, 0):
        return MarketSession.PRE_MARKET
    elif time(10, 0) <= br_time < time(17, 0):
        return MarketSession.REGULAR_SESSION
    elif time(17, 0) <= br_time < time(18, 0):
        return MarketSession.CLOSING_PHASE
    elif time(18, 0) <= br_time < time(19, 0):
        return MarketSession.AFTER_MARKET
    else:
        return MarketSession.OUT_OF_SESSION

def get_session_label(session: MarketSession) -> str:
    labels = {
        MarketSession.PRE_MARKET: "Pré-Mercado (Leilão)",
        MarketSession.REGULAR_SESSION: "Sessão Regular",
        MarketSession.CLOSING_PHASE: "Fase de Fechamento",
        MarketSession.AFTER_MARKET: "After-Market",
        MarketSession.OUT_OF_SESSION: "Fora de Pregão"
    }
    return labels.get(session, "Desconhecido")
