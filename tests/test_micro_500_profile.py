from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
import pandas as pd

from models.autonomous_paper_trading_config import AutonomousPaperTradingConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from models.live_paper_trading_result import LivePaperCandidate
from run_autonomous_ibkr_paper import (
    MICRO_500_SHADOW_CONFIRMATION,
    build_config,
    build_storage_prefix,
    require_confirmation,
)
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.entry_frequency_gate import EntryFrequencyGate
from services.ibkr.ibkr_autonomous_runtime_factory import (
    IbkrAutonomousRuntimeFactory,
)
from services.intelligence.indicator_builder import IndicatorBuilder
from services.live_paper_market_scanner import LivePaperMarketScanner
from services.portfolio_allocator import PortfolioAllocator
from services.risk.time_stop_service import TimeStopService
from services.trading_cost_estimator import TradingCostEstimator
from models.paper_position import PaperPosition


def micro_config() -> LivePaperTradingConfig:
    return build_config(
        execution_mode=AutonomousPaperTradingConfig.SHADOW,
        pricing_plan=LivePaperTradingConfig.TIERED_PRICING,
        capital_profile=LivePaperTradingConfig.MICRO_500,
        monthly_market_data_cost_eur=3.0,
    ).live_config


def candidate(symbol: str, entry: float, stop: float) -> LivePaperCandidate:
    plan = RiskPlan(
        symbol=symbol,
        entry_price=entry,
        stop_loss=stop,
        target_1=entry * 1.02,
        target_2=entry * 1.04,
        target_3=entry * 1.06,
        risk_percent=2.0,
        reward_percent=6.0,
        risk_reward_ratio=3.0,
        confidence=0.9,
    )
    pipeline = TradingPipelineResult(
        symbol=symbol,
        decision="BUY",
        confidence=0.9,
        position_size=150.0,
        expected_risk=1.0,
        risk_plan=plan,
        market_intelligence=None,
        ai_context=None,
        explanation=None,
    )
    return LivePaperCandidate(
        symbol=symbol,
        result=pipeline,
        score=90.0,
        accepted=True,
        reason="Accepted.",
    )


def test_micro_profile_has_isolated_realistic_capital_limits() -> None:
    config = micro_config()

    assert config.capital_profile == LivePaperTradingConfig.MICRO_500
    assert config.initial_cash == 500.0
    assert config.max_open_positions == 2
    assert config.max_new_positions_per_cycle == 1
    assert config.max_new_positions_per_day == 2
    assert config.max_position_value == 175.0
    assert config.min_cash_reserve_pct == 0.30
    assert config.max_holding_minutes == 90
    assert config.reentry_cooldown_minutes == 60
    assert config.history_period == "5d"
    assert config.history_interval == "5m"
    assert config.max_history_age_minutes == 10


def test_micro_profile_is_restricted_to_shadow_mode() -> None:
    with pytest.raises(ValueError, match="restricted to SHADOW"):
        AutonomousPaperTradingConfig(
            execution_mode=AutonomousPaperTradingConfig.BUY_AND_SELL,
            live_config=LivePaperTradingConfig(
                capital_profile=LivePaperTradingConfig.MICRO_500,
            ),
        )


def test_micro_runtime_uses_two_minute_intraday_cache() -> None:
    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id="DU1234567",
        config=build_config(
            execution_mode=AutonomousPaperTradingConfig.SHADOW,
            pricing_plan=LivePaperTradingConfig.TIERED_PRICING,
            news_mode=LivePaperTradingConfig.NEWS_DISABLED,
            capital_profile=LivePaperTradingConfig.MICRO_500,
            monthly_market_data_cost_eur=3.0,
        ),
        allow_order_submission=False,
    )

    assert runtime.historical_provider.cache.ttl.total_seconds() == 120


def test_micro_profile_uses_separate_shadow_storage_prefix() -> None:
    assert build_storage_prefix(
        execution_mode=AutonomousPaperTradingConfig.SHADOW,
        capital_profile=LivePaperTradingConfig.MICRO_500,
    ) == "data/orion_shadow_micro_500"
    assert build_storage_prefix(
        execution_mode=AutonomousPaperTradingConfig.SHADOW,
        capital_profile=LivePaperTradingConfig.STANDARD_10000,
    ) == "data/orion_shadow"


def test_micro_profile_uses_explicit_confirmation(monkeypatch) -> None:
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: MICRO_500_SHADOW_CONFIRMATION,
    )

    assert require_confirmation(
        AutonomousPaperTradingConfig.SHADOW,
        1,
        LivePaperTradingConfig.MICRO_500,
    ) is True


def test_market_data_budget_is_amortized_per_round_trip() -> None:
    estimate = TradingCostEstimator().estimate_round_trip(
        position=PaperPosition(
            symbol="F",
            quantity=3,
            entry_price=50.0,
            current_price=50.0,
            currency="USD",
            fx_rate_to_base=1.0,
        ),
        config=micro_config(),
    )

    assert estimate.market_data_overhead_eur == 0.08
    assert estimate.total_cost_eur == 1.27


def test_micro_economic_gate_rejects_unrealistic_european_trade() -> None:
    result = PortfolioAllocator().allocate(
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=500.0),
            peak_portfolio_value=500.0,
        ),
        candidates=[candidate("TEST.AS", 100.0, 99.0)],
        config=micro_config(),
    )

    assert result.approved_count == 0
    assert "estimated round-trip costs" in result.decisions[0].reason
    assert "above 2.00%" in result.decisions[0].reason


def test_micro_economic_gate_can_accept_liquid_us_sized_trade() -> None:
    result = PortfolioAllocator().allocate(
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=500.0),
            peak_portfolio_value=500.0,
        ),
        candidates=[candidate("F", 50.0, 49.0)],
        config=micro_config(),
    )

    assert result.approved_count == 1
    assert result.approved[0].quantity == 3


def test_entry_frequency_gate_enforces_daily_limit() -> None:
    now = datetime(2026, 7, 21, 12, 0, tzinfo=UTC)
    session = TradingSession(
        name="Micro",
        portfolio=PaperPortfolio(cash=500.0),
        position_states={
            "A": PositionState(
                symbol="A",
                entry_price=10.0,
                current_stop_loss=9.0,
                highest_price=10.0,
                current_price=10.0,
                trade_id="open-a",
                opened_at=now - timedelta(minutes=30),
            )
        },
    )
    completed = [
        SimpleNamespace(
            trade_id="closed-b",
            symbol="B",
            opened_at=now - timedelta(hours=2),
            closed_at=now - timedelta(hours=1),
        )
    ]

    decision = EntryFrequencyGate().evaluate(
        symbol="C",
        session=session,
        completed_trades=completed,
        max_new_positions_per_day=2,
        reentry_cooldown_minutes=60,
        now=now,
    )

    assert decision.allowed is False
    assert decision.entries_today == 2
    assert "Daily entry limit" in decision.reason


def test_entry_frequency_gate_enforces_symbol_cooldown() -> None:
    now = datetime(2026, 7, 21, 12, 0, tzinfo=UTC)
    completed = [
        SimpleNamespace(
            trade_id="closed-f",
            symbol="F",
            opened_at=now - timedelta(days=1),
            closed_at=now - timedelta(minutes=30),
        )
    ]

    decision = EntryFrequencyGate().evaluate(
        symbol="f",
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=500.0),
        ),
        completed_trades=completed,
        max_new_positions_per_day=2,
        reentry_cooldown_minutes=60,
        now=now,
    )

    assert decision.allowed is False
    assert "Re-entry cooldown" in decision.reason


def test_runner_applies_daily_entry_limit_to_accepted_candidates() -> None:
    now = datetime.now(UTC)
    completed = [
        SimpleNamespace(
            trade_id=f"trade-{index}",
            symbol=f"OLD{index}",
            opened_at=now - timedelta(hours=2),
            closed_at=now - timedelta(hours=1),
        )
        for index in range(2)
    ]
    repository = SimpleNamespace(load_all=lambda: completed)
    runner = AutonomousPaperTradingRunner(
        config=build_config(
            execution_mode=AutonomousPaperTradingConfig.SHADOW,
            pricing_plan=LivePaperTradingConfig.TIERED_PRICING,
            capital_profile=LivePaperTradingConfig.MICRO_500,
            monthly_market_data_cost_eur=3.0,
        ),
        completed_trade_repository=repository,
    )
    scan = SimpleNamespace(candidates=[candidate("F", 50.0, 49.0)])

    filtered = runner._apply_entry_frequency_limits(
        scan_result=scan,
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=500.0),
        ),
    )

    assert filtered.candidates[0].accepted is False
    assert "Daily entry limit" in filtered.candidates[0].reason


def test_micro_time_stop_activates_after_ninety_minutes() -> None:
    now = datetime(2026, 7, 21, 12, 0, tzinfo=UTC)
    state = PositionState(
        symbol="F",
        entry_price=10.0,
        current_stop_loss=9.0,
        highest_price=10.0,
        current_price=10.0,
        opened_at=now - timedelta(minutes=91),
    )

    result = TimeStopService().evaluate(
        state=state,
        maximum_days=2,
        maximum_minutes=90,
        now=now,
    )

    assert result.activated is True
    assert result.maximum_hours == 1.5
    assert "intraday" in result.reason


def test_intraday_history_drops_unfinished_candle() -> None:
    now = datetime(2026, 7, 21, 10, 2, tzinfo=UTC)
    scanner = LivePaperMarketScanner(
        config=micro_config(),
        clock=lambda: now,
    )
    history = intraday_history(now=now, last_offset_minutes=-2)

    prepared = scanner._prepare_history(
        symbol="F",
        history=history,
        evaluated_at=now,
    )

    assert len(prepared) == len(history) - 1
    assert prepared.index[-1] == now - timedelta(minutes=7)
    assert prepared.attrs["interval"] == "5m"


def test_intraday_history_rejects_stale_completed_candle() -> None:
    now = datetime(2026, 7, 21, 10, 0, tzinfo=UTC)
    scanner = LivePaperMarketScanner(
        config=micro_config(),
        clock=lambda: now,
    )
    history = intraday_history(now=now, last_offset_minutes=-30)

    with pytest.raises(ValueError, match="minutes old"):
        scanner._prepare_history(
            symbol="F",
            history=history,
            evaluated_at=now,
        )


def test_five_minute_indicators_use_intraday_scaling() -> None:
    close = pd.Series([100.0 + (index * 0.02) for index in range(40)])
    builder = IndicatorBuilder()

    assert builder._calculate_trend(
        close,
        interval="5m",
    ) > builder._calculate_trend(close, interval="1d")
    assert builder._calculate_momentum(
        close,
        interval="5m",
    ) > builder._calculate_momentum(close, interval="1d")

    volatile = pd.Series(
        [100.0, 100.2, 99.9, 100.3, 99.8] * 10,
        dtype=float,
    )
    assert builder._calculate_volatility(
        volatile,
        interval="5m",
    ) > builder._calculate_volatility(volatile, interval="1d")


def intraday_history(
    *,
    now: datetime,
    last_offset_minutes: int,
) -> pd.DataFrame:
    last = now + timedelta(minutes=last_offset_minutes)
    index = pd.date_range(
        end=last,
        periods=30,
        freq="5min",
        tz="UTC",
    )
    closes = [100.0 + (item * 0.02) for item in range(len(index))]
    return pd.DataFrame(
        {
            "Open": [value - 0.01 for value in closes],
            "High": [value + 0.05 for value in closes],
            "Low": [value - 0.05 for value in closes],
            "Close": closes,
            "Volume": [100_000.0] * len(index),
        },
        index=index,
    )
