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
from services.position_monitor import PositionMonitor
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
    assert config.max_open_positions == 1
    assert config.max_new_positions_per_cycle == 1
    assert config.max_new_positions_per_day == 1
    assert config.max_new_positions_per_week == 5
    assert config.max_position_value == 350.0
    assert config.min_cash_reserve_pct == 0.30
    assert config.max_holding_minutes == 180
    assert config.reentry_cooldown_minutes == 240
    assert config.allowed_entry_market_codes == ("XUSA",)
    assert config.entry_open_buffer_minutes == 15
    assert config.entry_close_buffer_minutes == 180
    assert config.require_intraday_confirmation is True
    assert config.history_period == "5d"
    assert config.history_interval == "5m"
    assert config.max_history_age_minutes == 15
    assert config.small_profit_target_us_eur == 4.5
    assert config.small_profit_max_loss_us_eur == 3.0
    assert config.min_net_reward_risk_ratio == 1.5
    assert config.max_required_gross_move_pct == 0.025


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


def test_micro_shadow_reconciles_legacy_gross_cash_to_completed_net() -> None:
    runner = AutonomousPaperTradingRunner(
        config=build_config(
            execution_mode=AutonomousPaperTradingConfig.SHADOW,
            pricing_plan=LivePaperTradingConfig.TIERED_PRICING,
            news_mode=LivePaperTradingConfig.NEWS_DISABLED,
            capital_profile=LivePaperTradingConfig.MICRO_500,
            monthly_market_data_cost_eur=3.0,
        ),
        completed_trade_repository=SimpleNamespace(
            load_all=lambda: [
                SimpleNamespace(estimated_net_profit_loss=-2.06),
                SimpleNamespace(estimated_net_profit_loss=0.20),
            ]
        ),
    )
    legacy_session = TradingSession(
        name="Legacy micro shadow",
        portfolio=PaperPortfolio(cash=500.54),
        peak_portfolio_value=500.54,
    )

    reconciled = runner._reconcile_micro_shadow_cash(legacy_session)

    assert reconciled.cash == 498.14
    assert reconciled.equity == 498.14
    assert reconciled.peak_portfolio_value == 500.0


def test_micro_shadow_does_not_reconcile_without_completed_trade_store() -> None:
    runner = AutonomousPaperTradingRunner(
        config=build_config(
            execution_mode=AutonomousPaperTradingConfig.SHADOW,
            capital_profile=LivePaperTradingConfig.MICRO_500,
        )
    )
    session = TradingSession(
        name="Micro without completed store",
        portfolio=PaperPortfolio(cash=490.0),
    )

    assert runner._reconcile_micro_shadow_cash(session) is session


def test_micro_shadow_exit_cost_is_deducted_from_portfolio_cash() -> None:
    runner = AutonomousPaperTradingRunner(
        config=build_config(
            execution_mode=AutonomousPaperTradingConfig.SHADOW,
            pricing_plan=LivePaperTradingConfig.TIERED_PRICING,
            news_mode=LivePaperTradingConfig.NEWS_DISABLED,
            capital_profile=LivePaperTradingConfig.MICRO_500,
            monthly_market_data_cost_eur=3.0,
        )
    )
    position = PaperPosition(
        symbol="F",
        quantity=3,
        entry_price=50.0,
        current_price=51.0,
        currency="USD",
        fx_rate_to_base=1.0,
    )
    gross_exit_portfolio = PaperPortfolio(cash=503.0)
    estimate = TradingCostEstimator().estimate_round_trip(
        position=position,
        config=runner.config.live_config,
    )

    net_portfolio = runner._apply_shadow_exit_cost(
        portfolio=gross_exit_portfolio,
        position=position,
        executed_price=51.0,
    )

    assert net_portfolio.cash == round(503.0 - estimate.total_cost_eur, 2)


def test_micro_target_does_not_take_cost_dominated_qcom_profit() -> None:
    small_move = PositionMonitor().evaluate(
        PaperPosition(
            symbol="QCOM",
            quantity=1,
            entry_price=171.92,
            current_price=173.89,
            currency="USD",
            fx_rate_to_base=(150.46 / 171.92),
        ),
        micro_config(),
    )

    assert small_move.action == "HOLD"
    assert small_move.estimated_net_profit_loss < 4.50

    qualified_move = PositionMonitor().evaluate(
        PaperPosition(
            symbol="QCOM",
            quantity=1,
            entry_price=171.92,
            current_price=180.0,
            currency="USD",
            fx_rate_to_base=(150.46 / 171.92),
        ),
        micro_config(),
    )

    assert qualified_move.action == "TAKE_PROFIT"
    assert qualified_move.estimated_net_profit_loss >= 4.50
    assert qualified_move.minimum_net_profit == 4.50


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

    assert estimate.market_data_overhead_eur == 0.25
    assert estimate.total_cost_eur == 1.44


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
    assert "above 0.60%" in result.decisions[0].reason


def test_micro_economic_gate_can_accept_liquid_us_sized_trade() -> None:
    result = PortfolioAllocator().allocate(
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=500.0),
            peak_portfolio_value=500.0,
        ),
        candidates=[candidate("F", 50.0, 49.7)],
        config=micro_config(),
    )

    assert result.approved_count == 1
    assert result.approved[0].quantity == 7


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


def test_entry_frequency_gate_enforces_weekly_limit() -> None:
    now = datetime(2026, 7, 23, 12, 0, tzinfo=UTC)
    completed = [
        SimpleNamespace(
            trade_id=f"weekly-{index}",
            symbol=f"OLD{index}",
            opened_at=now - timedelta(days=index + 1),
            closed_at=now - timedelta(days=index + 1, hours=-1),
        )
        for index in range(3)
    ]

    decision = EntryFrequencyGate().evaluate(
        symbol="F",
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=500.0),
        ),
        completed_trades=completed,
        max_new_positions_per_day=1,
        max_new_positions_per_week=3,
        reentry_cooldown_minutes=240,
        now=now,
    )

    assert decision.allowed is False
    assert decision.entries_this_week == 3
    assert "Weekly entry limit" in decision.reason


def test_micro_week_limit_allows_fifth_entry_on_a_new_day() -> None:
    now = datetime(2026, 7, 24, 12, 0, tzinfo=UTC)
    completed = [
        SimpleNamespace(
            trade_id=f"weekly-{index}",
            symbol=f"OLD{index}",
            opened_at=now - timedelta(days=(index % 3) + 1),
            closed_at=now - timedelta(days=(index % 3) + 1, hours=-1),
        )
        for index in range(4)
    ]

    decision = EntryFrequencyGate().evaluate(
        symbol="F",
        session=TradingSession(
            name="Micro",
            portfolio=PaperPortfolio(cash=493.24),
        ),
        completed_trades=completed,
        max_new_positions_per_day=1,
        max_new_positions_per_week=5,
        reentry_cooldown_minutes=240,
        now=now,
    )

    assert decision.allowed is True
    assert decision.entries_today == 0
    assert decision.entries_this_week == 4


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


def test_micro_time_stop_activates_after_three_hours() -> None:
    now = datetime(2026, 7, 21, 12, 0, tzinfo=UTC)
    state = PositionState(
        symbol="F",
        entry_price=10.0,
        current_stop_loss=9.0,
        highest_price=10.0,
        current_price=10.0,
        opened_at=now - timedelta(minutes=181),
    )

    result = TimeStopService().evaluate(
        state=state,
        maximum_days=2,
        maximum_minutes=180,
        now=now,
    )

    assert result.activated is True
    assert result.maximum_hours == 3.0
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


def test_intraday_history_accepts_yahoo_delay_after_candle_completion() -> None:
    now = datetime(2026, 7, 21, 10, 0, tzinfo=UTC)
    scanner = LivePaperMarketScanner(
        config=micro_config(),
        clock=lambda: now,
    )
    history = intraday_history(now=now, last_offset_minutes=-17)

    prepared = scanner._prepare_history(
        symbol="F",
        history=history,
        evaluated_at=now,
    )

    assert prepared.index[-1] == now - timedelta(minutes=17)


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
