from __future__ import annotations

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import LivePaperCandidate
from models.paper_portfolio import PaperPortfolio
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from services.portfolio_allocator import PortfolioAllocator


def _candidate(
    symbol: str,
    price: float,
    confidence: float,
    score: float,
    accepted: bool = True,
) -> LivePaperCandidate:
    risk_plan = RiskPlan(
        symbol=symbol,
        entry_price=price,
        stop_loss=price * 0.95,
        target_1=price * 1.05,
        target_2=price * 1.10,
        target_3=price * 1.15,
        risk_percent=5.0,
        reward_percent=15.0,
        risk_reward_ratio=3.0,
        confidence=confidence,
        notes="Test risk plan",
    )

    result = TradingPipelineResult(
        symbol=symbol,
        decision="BUY",
        confidence=confidence,
        position_size=100.0,
        expected_risk=1.0,
        risk_plan=risk_plan,
        market_intelligence=None,
        ai_context=None,
        explanation=None,
    )

    return LivePaperCandidate(
        symbol=symbol,
        result=result,
        score=score,
        accepted=accepted,
        reason=(
            "Accepted candidate."
            if accepted
            else "Rejected test candidate."
        ),
    )


def main():
    session = TradingSession(
        name="Allocator Test",
        portfolio=PaperPortfolio(
            cash=500.0,
        ),
    )

    config = LivePaperTradingConfig(
        initial_cash=500.0,
        max_symbols=5,
        max_open_positions=2,
        min_confidence=0.75,
        max_position_value=150.0,
        max_position_size_pct=0.30,
    )

    candidates = [
        _candidate("AAA", price=50.0, confidence=0.95, score=95.0),
        _candidate("BBB", price=75.0, confidence=0.90, score=90.0),
        _candidate("CCC", price=100.0, confidence=0.85, score=85.0),
        _candidate(
            "DDD",
            price=25.0,
            confidence=0.80,
            score=80.0,
            accepted=False,
        ),
    ]

    allocator = PortfolioAllocator()

    result = allocator.allocate(
        session=session,
        candidates=candidates,
        config=config,
    )

    assert result.approved_count == 2
    assert result.rejected_count == 2

    approved_symbols = [
        decision.symbol
        for decision in result.approved
    ]

    assert approved_symbols == ["AAA", "BBB"]

    first = result.approved[0]
    second = result.approved[1]

    assert first.quantity == 3
    assert first.estimated_value == 150.0

    assert second.quantity == 2
    assert second.estimated_value == 150.0

    rejected_reasons = [
        decision.reason
        for decision in result.rejected
    ]

    assert "Maximum open positions reached." in rejected_reasons
    assert "Rejected test candidate." in rejected_reasons

    print("PORTFOLIO ALLOCATOR: PASS ✅")


if __name__ == "__main__":
    main()