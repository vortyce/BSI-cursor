import sys
import os
import argparse
from datetime import datetime, timedelta

# Add parent directory to sys.path
sys.path.append(os.getcwd())

from app.db.session import engine
from app.db.base import Base
from app.models.raw_webhook_log import RawWebhookLog
from app.models.signal import Signal
from app.models.signal_interpretation import SignalInterpretation
from app.models.signal_outcome import SignalOutcome
from app.models.portfolio_profile import PortfolioProfile
from app.models.allocation_recommendation import AllocationRecommendation
from app.models.allocation_item import AllocationItem
from app.models.portfolio_position import PortfolioPosition
from app.models.portfolio_review import PortfolioReview
from app.models.portfolio_action_item import PortfolioActionItem
from app.models.portfolio_decision import PortfolioDecision
from app.enums.signal import (
    SignalStatus, InterpretationStatus, DataSourceQuality, 
    ThesisCategory, SignalDomain
)
from app.enums.portfolio import (
    RiskProfile, PrimaryGoal, TimeHorizon, ManagementStyle,
    PositionStatus, PortfolioActionType, RecommendationStatus
)
from app.enums.decision import UserChoice, SimulatedExecutionStatus
from app.services.portfolio_service import PortfolioService
from app.core.seed_data import CRYPTO_SCENARIOS, B3_SCENARIOS, DEFAULT_PROFILE

from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

def create_full_scenario(session, domain, ext_id, asset, direction, price, interp_status_val, conf, align, regime, out_status, ret, thesis=None):
    raw = RawWebhookLog(raw_body="{}", parse_status="SIGNAL_CREATED")
    session.add(raw); session.flush()
    
    sig = Signal(
        raw_log_id=raw.id, 
        payload_version="1.0",
        external_signal_id=ext_id, 
        domain=domain,
        asset=asset, 
        market="BINANCE" if domain == SignalDomain.CRYPTO_SPOT else "B3",
        timeframe="15",
        signal_type="ENTRY",
        signal_direction=direction, 
        trigger_price=price, 
        signal_timestamp=datetime.utcnow(),
        strategy_name="BSI_Alpha", 
        strategy_version="1.0", 
        indicator_snapshot_json={},
        candle_context_json={},
        status=SignalStatus.INTERPRETED if interp_status_val == "SUCCESS" else SignalStatus.STORED
    )
    session.add(sig); session.flush()
    
    if interp_status_val:
        itp = SignalInterpretation(
            signal_id=sig.id, 
            llm_provider="OPENAI",
            llm_model="gpt-4o",
            prompt_version="v5",
            status=InterpretationStatus.SUCCESS if interp_status_val == "SUCCESS" else InterpretationStatus.FAILED, 
            confidence_level=conf, 
            confidence_score=90 if conf == "HIGH" else 60 if conf == "MEDIUM" else 30,
            context_alignment=align, 
            regime=regime, 
            primary_thesis=thesis or ThesisCategory.UNCLEAR_CONTEXT,
            rationale_short=f"Cenário {domain} - {conf} para demo.",
            raw_response_body="{}"
        )
        session.add(itp)
    
    if out_status != "OPEN":
        out = SignalOutcome(
            signal_id=sig.id, outcome_status=out_status, evaluation_method="TRADINGVIEW_FOLLOWUP",
            data_quality=DataSourceQuality.SEEDED_DEMO,
            entry_reference_price=price, resolution_price=price * (1 + ret/100),
            final_return_pct=ret, bars_to_resolution=15, resolved_at=datetime.utcnow()
        )
        session.add(out)
    
    return sig

def seed_crypto(session):
    print("Seed: Modo Crypto Spot")
    for s in CRYPTO_SCENARIOS:
        create_full_scenario(session, SignalDomain.CRYPTO_SPOT, **s)

def seed_b3(session):
    print("Seed: Modo B3 Equities")
    for s in B3_SCENARIOS:
        create_full_scenario(session, SignalDomain.B3_EQUITIES, **s)

def seed_portfolio(session):
    print("Seed: Configuração de Portfolio e Alocação")
    # Perfil moderado do seed_data
    profile = PortfolioProfile(
        initial_capital=DEFAULT_PROFILE["initial_capital"],
        risk_profile=RiskProfile[DEFAULT_PROFILE["risk_profile"]],
        primary_goal=PrimaryGoal[DEFAULT_PROFILE["primary_goal"]],
        horizon=TimeHorizon[DEFAULT_PROFILE["horizon"]],
        allowed_domains=DEFAULT_PROFILE["allowed_domains"],
        max_single_position_pct=DEFAULT_PROFILE["max_single_position_pct"],
        max_domain_exposure_pct=DEFAULT_PROFILE["max_domain_exposure_pct"],
        keep_cash_reserve_pct=DEFAULT_PROFILE["keep_cash_reserve_pct"],
        management_style=ManagementStyle[DEFAULT_PROFILE["management_style"]]
    )
    session.add(profile)
    session.flush()
    
    # Rodar motor de alocação
    PortfolioService.run_allocation_engine(session, profile.id)

def seed_live_portfolio(session):
    print("Seed: Gestão de Carteira Viva (Fase 10)")
    
    # 1. Obter Perfil
    profile = session.query(PortfolioProfile).first()
    if not profile:
        print("Erro: Perfil não encontrado para seed Phase 10")
        return

    # 2. Criar Posições Ativas (Cenário Base)
    # BTC (Saudável)
    sig_btc = session.query(Signal).filter(Signal.asset == "BTCUSD").first()
    if sig_btc:
        pos_btc = PortfolioPosition(
            signal_id=sig_btc.id,
            entry_price=65000.0,
            allocated_capital=1500.0, # 15% (Limite Máximo)
            status=PositionStatus.ACTIVE,
            entry_rationale="Entrada baseada em tendência forte detectada na Fase 9."
        )
        session.add(pos_btc)

    # PETR4 (Saudável)
    sig_petr = session.query(Signal).filter(Signal.asset == "PETR4").first()
    if sig_petr:
        pos_petr = PortfolioPosition(
            signal_id=sig_petr.id,
            entry_price=35.50,
            allocated_capital=1000.0, # 10%
            status=PositionStatus.ACTIVE,
            entry_rationale="Alinhamento com setor de energia B3."
        )
        session.add(pos_petr)

    # 3. Cenário: Excesso de Domínio B3
    sig_vale = session.query(Signal).filter(Signal.asset == "VALE3").first()
    if sig_vale:
        pos_vale = PortfolioPosition(
            signal_id=sig_vale.id,
            entry_price=62.20,
            allocated_capital=6000.0, # 60% -> Total B3 será 70%, estourando o limite de 60%
            status=PositionStatus.ACTIVE,
            entry_rationale="Posição grande para simular diagnóstico de excesso de domínio."
        )
        session.add(pos_vale)

    # 4. Cenário: Oportunidade Superior
    create_full_scenario(session, SignalDomain.CRYPTO_SPOT, "S-SUP-001", "SOLUSD", "LONG", 145.0, "SUCCESS", "HIGH", "ALIGNED", "BULLISH", "OPEN", 0.0, ThesisCategory.TREND_ALIGNED)

    session.commit()
    
    # 5. Rodar primeiro Review de diagnóstico
    from app.services.portfolio_review_service import PortfolioReviewService
    PortfolioReviewService.run_portfolio_review(session, profile.id)

def seed_governance(session):
    print("Seed: Governança e Histórico de Decisões (Fase 11)")
    
    # 1. Obter Action Items pendentes
    review = session.query(PortfolioReview).order_by(PortfolioReview.created_at.desc()).first()
    if not review:
        print("Erro: Review não encontrado para seed Phase 11")
        return

    # 2. Cenário: Decisão ACCEPTED (REPLACE)
    item_replace = session.query(PortfolioActionItem).filter(
        PortfolioActionItem.review_id == review.id,
        PortfolioActionItem.action_type == PortfolioActionType.REPLACE
    ).first()
    
    if item_replace:
        from app.services.decision_service import DecisionService
        DecisionService.record_user_choice(session, item_replace.id, UserChoice.ACCEPTED, "Aceito a troca. SOL parece mais forte no curto prazo.")
        print("  -> Decisão ACCEPTED registrada para REPLACE")

    # 3. Cenário: Decisão REJECTED (REDUCE)
    item_reduce = session.query(PortfolioActionItem).filter(
        PortfolioActionItem.review_id == review.id,
        PortfolioActionItem.action_type == PortfolioActionType.REDUCE
    ).first()
    
    if item_reduce:
        from app.services.decision_service import DecisionService
        DecisionService.record_user_choice(session, item_reduce.id, UserChoice.REJECTED, "Prefiro manter a exposição atual apesar do drift.")
        print("  -> Decisão REJECTED registrada para REDUCE")

    # 4. Cenário: Decisão DEFERRED
    item_deferred = PortfolioActionItem(
        review_id=review.id,
        action_type=PortfolioActionType.HOLD,
        rationale="Posição em observação.",
        created_at=datetime.utcnow()
    )
    session.add(item_deferred); session.flush()
    
    from app.services.decision_service import DecisionService
    DecisionService.record_user_choice(session, item_deferred.id, UserChoice.DEFERRED, "Vou aguardar o fechamento do candle diário para decidir.")
    print("  -> Decisão DEFERRED registrada")

    # 5. Cenário: Recomendação EXPIRED
    item_expired = PortfolioActionItem(
        review_id=review.id,
        action_type=PortfolioActionType.INCREASE,
        rationale="Oportunidade de aumento de posição ignorada.",
        created_at=datetime.utcnow() - timedelta(days=5)
    )
    session.add(item_expired); session.flush()
    
    DecisionService.record_user_choice(session, item_expired.id, UserChoice.EXPIRED, "Sistema expirou automaticamente por falta de resposta em 48h.")
    print("  -> Decisão EXPIRED registrada")

    session.commit()

def main():
    parser = argparse.ArgumentParser(description="BSI Database Seeder - Phase 11.5 Refactored")
    parser.add_argument("--mode", choices=["crypto_demo", "b3_demo", "all_demo", "minimal"], default="all_demo", help="Modo de população")
    parser.add_argument("--clean", action="store_true", help="Limpar banco antes de popular")
    args = parser.parse_args()

    with Session(engine) as session:
        if args.clean:
            print("Limpando banco de dados...")
            session.query(SignalOutcome).delete()
            session.query(SignalInterpretation).delete()
            session.query(Signal).delete()
            session.query(RawWebhookLog).delete()
            session.query(PortfolioDecision).delete()
            session.query(PortfolioActionItem).delete()
            session.query(PortfolioReview).delete()
            session.query(PortfolioPosition).delete()
            session.query(AllocationItem).delete()
            session.query(AllocationRecommendation).delete()
            session.query(PortfolioProfile).delete()
            session.commit()

        if args.mode in ["crypto_demo", "all_demo"]:
            seed_crypto(session)
        
        if args.mode in ["b3_demo", "all_demo"]:
            seed_b3(session)
        
        if args.mode == "all_demo":
            seed_portfolio(session)
            seed_live_portfolio(session)
            seed_governance(session)
            
        if args.mode == "minimal":
            create_full_scenario(session, SignalDomain.CRYPTO_SPOT, "MIN-001", "BTCUSD", "LONG", 60000, "SUCCESS", "HIGH", "ALIGNED", "BULLISH", "WIN", 2.0, ThesisCategory.TREND_ALIGNED)

        session.commit()
        print(f"Banco de dados populado com sucesso (modo: {args.mode})")

if __name__ == "__main__":
    main()
