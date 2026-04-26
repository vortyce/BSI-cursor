from app.enums.signal import SignalDomain, ThesisCategory

CRYPTO_SCENARIOS = [
    {
        "ext_id": "C-001", "asset": "BTCUSD", "direction": "LONG", "price": 65000, 
        "interp_status_val": "SUCCESS", "conf": "HIGH", "align": "ALIGNED", "regime": "BULLISH", "out_status": "WIN", 
        "ret": 3.2, "thesis": ThesisCategory.TREND_ALIGNED
    },
    {
        "ext_id": "C-002", "asset": "ETHUSD", "direction": "SHORT", "price": 3500, 
        "interp_status_val": "SUCCESS", "conf": "HIGH", "align": "ALIGNED", "regime": "BEARISH", "out_status": "WIN", 
        "ret": 2.8, "thesis": ThesisCategory.TREND_ALIGNED
    },
    {
        "ext_id": "C-003", "asset": "SOLUSD", "direction": "LONG", "price": 150, 
        "interp_status_val": "SUCCESS", "conf": "LOW", "align": "CONFLICTING", "regime": "RANGE", "out_status": "LOSS", 
        "ret": -4.5, "thesis": ThesisCategory.RANGE_CONFLICT
    }
]

B3_SCENARIOS = [
    {
        "ext_id": "B3-001", "asset": "PETR4", "direction": "LONG", "price": 35.50, 
        "interp_status_val": "SUCCESS", "conf": "LOW", "align": "CONFLICTING", "regime": "REGULAR_SESSION", "out_status": "WIN", 
        "ret": 1.5, "thesis": ThesisCategory.TREND_ALIGNED
    },
    {
        "ext_id": "B3-002", "asset": "VALE3", "direction": "SHORT", "price": 62.20, 
        "interp_status_val": "SUCCESS", "conf": "MEDIUM", "align": "ALIGNED", "regime": "REGULAR_SESSION", "out_status": "WIN", 
        "ret": 0.8, "thesis": ThesisCategory.TREND_ALIGNED
    },
    {
        "ext_id": "B3-003", "asset": "ITUB4", "direction": "LONG", "price": 33.10, 
        "interp_status_val": "SUCCESS", "conf": "LOW", "align": "CONFLICTING", "regime": "PRE_MARKET", "out_status": "LOSS", 
        "ret": -1.2, "thesis": ThesisCategory.VOLATILITY_WARNING
    }
]

DEFAULT_PROFILE = {
    "initial_capital": 10000.0,
    "risk_profile": "MODERATE",
    "primary_goal": "GROWTH",
    "horizon": "MEDIUM",
    "allowed_domains": ["CRYPTO_SPOT", "B3_EQUITIES"],
    "max_single_position_pct": 15.0,
    "max_domain_exposure_pct": 60.0,
    "keep_cash_reserve_pct": 25.0,
    "management_style": "TACTICAL"
}
