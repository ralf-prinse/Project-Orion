from __future__ import annotations

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from test_autonomous_broker_exit_lifecycle import (
    FakePositionExitExecutionService,
    create_session,
)
from run_autonomous_ibkr_paper import build_config


class ScannerMustNotRun:
    def run(self, **kwargs):
        raise AssertionError("EXIT_ONLY must not start the BUY scanner.")


class TradingCycleMustNotRun:
    def run(self, **kwargs):
        raise AssertionError("EXIT_ONLY must not enter BUY execution.")


class InMemorySessionRepository:
    def __init__(self, session) -> None:
        self.session = session
        self.saved = []

    def exists(self) -> bool:
        return True

    def load(self):
        return self.session

    def save(self, session) -> None:
        self.session = session
        self.saved.append(session)


class FixedPriceProvider:
    def get_current_price(self, symbol: str) -> float:
        return 94.0


def exit_only_config() -> AutonomousPaperTradingConfig:
    return AutonomousPaperTradingConfig(
        execution_mode=AutonomousPaperTradingConfig.EXIT_ONLY,
        cycles=1,
        sleep_seconds=0.0,
        stop_on_exception=True,
        print_cycle_summary=False,
    )


def test_exit_only_skips_scanner_allocator_and_buy_execution() -> None:
    repository = InMemorySessionRepository(create_session())
    runner = AutonomousPaperTradingRunner(
        config=exit_only_config(),
        scanner=ScannerMustNotRun(),
        trading_cycle=TradingCycleMustNotRun(),
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(),
        position_exit_execution_service=(
            FakePositionExitExecutionService()
        ),
    )

    result = runner.run()

    assert result.completed_cycles == 1
    assert result.failed_cycles == 0
    assert result.total_executed_trades == 0
    assert result.cycle_results[0].scan.scanned_symbols == 0
    assert result.cycle_results[0].allocation.decisions == []


def test_exit_only_allows_managed_sell_execution() -> None:
    repository = InMemorySessionRepository(create_session())
    exit_service = FakePositionExitExecutionService()
    runner = AutonomousPaperTradingRunner(
        config=exit_only_config(),
        scanner=ScannerMustNotRun(),
        trading_cycle=TradingCycleMustNotRun(),
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(),
        position_exit_execution_service=exit_service,
    )

    result = runner.run()

    assert exit_service.execute_calls == 1
    assert result.total_executed_exits == 1
    assert result.session.open_positions == 0
    assert repository.saved


def test_ibkr_entrypoint_defaults_to_exit_only_and_twenty_positions() -> None:
    config = build_config()

    assert config.execution_mode == AutonomousPaperTradingConfig.EXIT_ONLY
    assert config.live_config.max_open_positions == 20
    assert config.live_config.max_portfolio_exposure == 0.90
    assert config.live_config.max_portfolio_risk_pct == 0.06
    assert config.live_config.min_cash_reserve_pct == 0.10


def test_invalid_execution_mode_is_rejected() -> None:
    try:
        AutonomousPaperTradingConfig(execution_mode="INVALID")
    except ValueError as exc:
        assert "EXIT_ONLY or BUY_AND_SELL" in str(exc)
    else:
        raise AssertionError("Expected invalid execution mode to fail.")
