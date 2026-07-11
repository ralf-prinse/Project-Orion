from __future__ import annotations

from pathlib import Path

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


SESSION_PATH = Path(
    "data/smoke_crash_recovery_session.json"
)


class FailOnceScanner:
    def __init__(self):
        self.calls = 0

    def run(self, session):
        self.calls += 1

        if self.calls == 1:
            raise RuntimeError(
                "Simulated scanner crash."
            )

        return type(
            "ScanResult",
            (),
            {
                "candidates": [],
                "scanned_symbols": 0,
            },
        )()


class FixedPriceProvider:
    def get_current_price(
        self,
        symbol: str,
    ) -> float:
        return 106.0


def build_seed_session() -> TradingSession:
    return TradingSession(
        name="Orion Crash Recovery Smoke Test",
        portfolio=PaperPortfolio(
            cash=400.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=1,
                    entry_price=100.0,
                    current_price=100.0,
                ),
            },
        ),
        position_states={
            "AAPL": PositionState(
                symbol="AAPL",
                entry_price=100.0,
                current_stop_loss=95.0,
                highest_price=100.0,
                current_price=100.0,
                break_even_active=False,
                trailing_stop_active=False,
                target_1_hit=False,
                target_2_hit=False,
                target_3_hit=False,
            ),
        },
        risk_plans={
            "AAPL": RiskPlan(
                symbol="AAPL",
                entry_price=100.0,
                stop_loss=95.0,
                target_1=104.0,
                target_2=112.0,
                target_3=120.0,
                risk_percent=5.0,
                reward_percent=20.0,
                risk_reward_ratio=4.0,
                confidence=0.90,
                notes="Crash recovery smoke test.",
            ),
        },
        status="ACTIVE",
    )


def build_runner(
    repository: JsonTradingSessionRepository,
    scanner: FailOnceScanner,
) -> ContinuousPaperTradingRunner:
    autonomous_config = AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=500.0,
            max_symbols=1,
        ),
        print_cycle_summary=False,
    )

    autonomous_runner = AutonomousPaperTradingRunner(
        config=autonomous_config,
        scanner=scanner,
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(),
    )

    continuous_config = ContinuousRunnerConfig(
        autonomous_config=autonomous_config,
        interval_seconds=1,
        max_iterations=2,
        stop_on_exception=False,
        print_iteration_summary=True,
    )

    return ContinuousPaperTradingRunner(
        config=continuous_config,
        runner=autonomous_runner,
    )


def validate_seed_session(
    session: TradingSession,
) -> None:
    position = session.portfolio.positions["AAPL"]
    state = session.position_states["AAPL"]

    assert position.current_price == 100.0
    assert state.current_price == 100.0
    assert state.current_stop_loss == 95.0
    assert state.break_even_active is False
    assert state.trailing_stop_active is False


def validate_recovered_session(
    session: TradingSession,
) -> None:
    position = session.portfolio.positions["AAPL"]
    state = session.position_states["AAPL"]

    assert position.current_price == 106.0
    assert state.current_price == 106.0
    assert state.highest_price == 106.0
    assert state.current_stop_loss == 100.7
    assert state.break_even_active is True
    assert state.trailing_stop_active is True
    assert state.target_1_hit is True
    assert "AAPL" in session.risk_plans


def main() -> None:
    repository = JsonTradingSessionRepository(
        path=SESSION_PATH,
    )

    repository.delete()
    repository.save(build_seed_session())

    print()
    print("=========================================")
    print("ORION CRASH RECOVERY SMOKE TEST")
    print("=========================================")
    print()

    before = repository.load()
    validate_seed_session(before)

    scanner = FailOnceScanner()
    runner = build_runner(
        repository=repository,
        scanner=scanner,
    )

    result = runner.run()

    recovered = repository.load()
    validate_recovered_session(recovered)

    assert scanner.calls == 2
    assert result.iterations_completed == 1
    assert result.failed_iterations == 1
    assert result.last_result is not None
    assert result.last_result.failed_cycles == 0

    print()
    print("CRASH RECOVERY RESULT")
    print("---------------------")
    print(f"Scanner calls:        {scanner.calls}")
    print(f"Completed iterations: {result.iterations_completed}")
    print(f"Failed iterations:    {result.failed_iterations}")
    print(f"Recovered price:      EUR {recovered.portfolio.positions['AAPL'].current_price:.2f}")
    print(f"Recovered stop:       EUR {recovered.position_states['AAPL'].current_stop_loss:.2f}")
    print()
    print("CRASH RECOVERY: PASS")

    repository.delete()


if __name__ == "__main__":
    main()
