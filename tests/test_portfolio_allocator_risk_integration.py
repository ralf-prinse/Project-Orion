from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import LivePaperCandidate
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from services.portfolio_allocator import PortfolioAllocator


def _candidate(
    symbol: str,
    *,
    entry_price: float = 100.0,
    stop_loss: float = 95.0,
    score: float = 90.0,
) -> LivePaperCandidate:
    risk_plan = RiskPlan(
        symbol=symbol,
        entry_price=entry_price,
        stop_loss=stop_loss,
        target_1=110.0,
        target_2=115.0,
        target_3=120.0,
        risk_percent=5.0,
        reward_percent=15.0,
        risk_reward_ratio=3.0,
        confidence=0.90,
    )
    result = TradingPipelineResult(
        symbol=symbol,
        decision="BUY",
        confidence=0.90,
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
        accepted=True,
        reason="Accepted candidate.",
    )


def _config(**overrides) -> LivePaperTradingConfig:
    values = {
        "initial_cash": 1_000.0,
        "max_open_positions": 10,
        "max_position_value": 500.0,
        "max_position_size_pct": 0.50,
        "max_portfolio_exposure": 1.0,
        "min_cash_reserve_pct": 0.0,
        "max_risk_per_trade_pct": 0.10,
        "max_portfolio_risk_pct": 0.20,
        "max_drawdown_pct": 0.20,
    }
    values.update(overrides)
    return LivePaperTradingConfig(**values)


def test_allocator_blocks_risk_per_trade_limit() -> None:
    session = TradingSession(
        name="Trade risk gate",
        portfolio=PaperPortfolio(cash=1_000.0),
        peak_portfolio_value=1_000.0,
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA", stop_loss=90.0)],
        config=_config(max_risk_per_trade_pct=0.01),
    )

    assert result.approved_count == 0
    assert "risk per trade limit exceeded" in result.rejected[0].reason


def test_allocator_tracks_risk_across_approved_candidates() -> None:
    session = TradingSession(
        name="Cumulative risk gate",
        portfolio=PaperPortfolio(cash=1_000.0),
        peak_portfolio_value=1_000.0,
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[
            _candidate("AAA", stop_loss=80.0, score=100.0),
            _candidate("BBB", stop_loss=80.0, score=90.0),
        ],
        config=_config(
            max_position_value=100.0,
            max_position_size_pct=0.10,
            max_risk_per_trade_pct=0.03,
            max_portfolio_risk_pct=0.03,
        ),
    )

    assert [decision.symbol for decision in result.approved] == ["AAA"]
    assert [decision.symbol for decision in result.rejected] == ["BBB"]
    assert "total portfolio risk limit exceeded" in result.rejected[0].reason


def test_allocator_includes_existing_managed_position_risk() -> None:
    risk_plan = _candidate("OPEN", stop_loss=90.0).result.risk_plan
    session = TradingSession(
        name="Existing portfolio risk gate",
        portfolio=PaperPortfolio(
            cash=500.0,
            positions={
                "OPEN": PaperPosition(
                    symbol="OPEN",
                    quantity=5,
                    entry_price=100.0,
                    current_price=100.0,
                )
            },
        ),
        position_states={
            "OPEN": PositionState(
                symbol="OPEN",
                entry_price=100.0,
                current_stop_loss=90.0,
                highest_price=100.0,
                current_price=100.0,
            )
        },
        risk_plans={"OPEN": risk_plan},
        peak_portfolio_value=1_000.0,
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("NEW", stop_loss=95.0)],
        config=_config(
            max_position_value=100.0,
            max_position_size_pct=0.10,
            max_portfolio_risk_pct=0.052,
        ),
    )

    assert result.approved_count == 0
    assert "total portfolio risk limit exceeded" in result.rejected[0].reason


def test_allocator_blocks_when_drawdown_limit_is_exceeded() -> None:
    session = TradingSession(
        name="Drawdown risk gate",
        portfolio=PaperPortfolio(cash=800.0),
        peak_portfolio_value=1_000.0,
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA")],
        config=_config(max_drawdown_pct=0.10),
    )

    assert result.approved_count == 0
    assert "maximum drawdown exceeded" in result.rejected[0].reason


def test_allocator_fails_closed_for_unmanaged_open_position() -> None:
    session = TradingSession(
        name="Unmanaged position risk gate",
        portfolio=PaperPortfolio(
            cash=500.0,
            positions={
                "EXTERNAL": PaperPosition(
                    symbol="EXTERNAL",
                    quantity=5,
                    entry_price=100.0,
                    current_price=100.0,
                )
            },
        ),
        peak_portfolio_value=1_000.0,
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("NEW")],
        config=_config(max_position_size_pct=0.10),
    )

    assert result.approved_count == 0
    assert "EXTERNAL has no managed RiskPlan" in result.rejected[0].reason


def test_allocator_rejects_invalid_buy_stop_loss() -> None:
    session = TradingSession(
        name="Invalid stop risk gate",
        portfolio=PaperPortfolio(cash=1_000.0),
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA", stop_loss=100.0)],
        config=_config(),
    )

    assert result.approved_count == 0
    assert "BUY stop-loss" in result.rejected[0].reason


def test_allocator_rejects_non_finite_risk_prices() -> None:
    session = TradingSession(
        name="Non-finite risk gate",
        portfolio=PaperPortfolio(cash=1_000.0),
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA", stop_loss=float("nan"))],
        config=_config(),
    )

    assert result.approved_count == 0
    assert "BUY stop-loss" in result.rejected[0].reason


def test_allocator_reports_cash_reserve_rejection() -> None:
    session = TradingSession(
        name="Cash reserve gate",
        portfolio=PaperPortfolio(cash=1_000.0),
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA")],
        config=_config(min_cash_reserve_pct=1.0),
    )

    assert result.approved_count == 0
    assert result.rejected[0].reason == "Cash reserve reached."


def test_allocator_reports_position_exposure_rejection() -> None:
    session = TradingSession(
        name="Position exposure gate",
        portfolio=PaperPortfolio(cash=1_000.0),
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA")],
        config=_config(max_position_size_pct=0.05),
    )

    assert result.approved_count == 0
    assert (
        result.rejected[0].reason
        == "Maximum position exposure does not allow a whole share."
    )


def test_allocator_reports_total_exposure_rejection() -> None:
    session = TradingSession(
        name="Total exposure gate",
        portfolio=PaperPortfolio(
            cash=500.0,
            positions={
                "OPEN": PaperPosition(
                    symbol="OPEN",
                    quantity=5,
                    entry_price=100.0,
                    current_price=100.0,
                )
            },
        ),
    )

    result = PortfolioAllocator().allocate(
        session=session,
        candidates=[_candidate("AAA")],
        config=_config(max_portfolio_exposure=0.50),
    )

    assert result.approved_count == 0
    assert (
        result.rejected[0].reason
        == "Maximum portfolio exposure reached."
    )
