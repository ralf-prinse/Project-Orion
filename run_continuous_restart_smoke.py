from __future__ import annotations

import argparse
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


SESSION_PATH = Path("data/smoke_trading_session.json")


class EmptyScanner:
    def run(self, session):
        return type(
            "ScanResult",
            (),
            {
                "candidates": [],
                "scanned_symbols": 0,
            },
        )()


class FixedPriceProvider:
    def __init__(self, price: float):
        self.price = float(price)

    def get_current_price(self, symbol: str) -> float:
        return self.price


def build_seed_session() -> TradingSession:
    return TradingSession(
        name="Orion Restart Exit Recovery Smoke Test",
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
                notes="Restart exit recovery smoke test.",
            ),
        },
        status="ACTIVE",
    )


def build_runner(
    repository: JsonTradingSessionRepository,
    iterations: int,
    interval: int,
    price: float,
) -> ContinuousPaperTradingRunner:
    autonomous_config = AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=500.0,
            max_symbols=1,
            take_profit_percent=0.05,
            stop_loss_percent=0.04,
        ),
        print_cycle_summary=True,
    )

    autonomous_runner = AutonomousPaperTradingRunner(
        config=autonomous_config,
        scanner=EmptyScanner(),
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(price),
    )

    continuous_config = ContinuousRunnerConfig(
        autonomous_config=autonomous_config,
        interval_seconds=interval,
        max_iterations=iterations,
        stop_on_exception=False,
        print_iteration_summary=True,
    )

    return ContinuousPaperTradingRunner(
        config=continuous_config,
        runner=autonomous_runner,
    )


def print_session(
    label: str,
    session: TradingSession,
) -> None:
    print()
    print(label)
    print("-" * len(label))
    print(f"Cash:            EUR {session.cash:.2f}")
    print(f"Equity:          EUR {session.equity:.2f}")
    print(f"Open positions:  {len(session.portfolio.positions)}")
    print(f"Position states: {len(session.position_states)}")
    print(f"Risk plans:      {len(session.risk_plans)}")

    if "AAPL" in session.portfolio.positions:
        position = session.portfolio.positions["AAPL"]
        state = session.position_states["AAPL"]
        plan = session.risk_plans["AAPL"]

        print(f"AAPL price:      EUR {position.current_price:.2f}")
        print(f"AAPL stop:       EUR {state.current_stop_loss:.2f}")
        print(f"AAPL high:       EUR {state.highest_price:.2f}")
        print(f"Break-even:      {state.break_even_active}")
        print(f"Trailing stop:   {state.trailing_stop_active}")
        print(f"Target 1 hit:    {state.target_1_hit}")
        print(f"Target 2 hit:    {state.target_2_hit}")
        print(f"Target 3 hit:    {state.target_3_hit}")
        print(f"Final target:    EUR {plan.target_3:.2f}")


def validate_managed_position(
    session: TradingSession,
) -> None:
    assert "AAPL" in session.portfolio.positions
    assert "AAPL" in session.position_states
    assert "AAPL" in session.risk_plans

    position = session.portfolio.positions["AAPL"]
    state = session.position_states["AAPL"]
    plan = session.risk_plans["AAPL"]

    assert position.current_price == 106.0
    assert state.current_price == 106.0
    assert state.highest_price == 106.0
    assert state.target_1_hit is True
    assert state.break_even_active is True
    assert state.trailing_stop_active is True
    assert state.current_stop_loss == 100.7
    assert plan.target_3 == 120.0


def validate_closed_session(
    session: TradingSession,
) -> None:
    assert "AAPL" not in session.portfolio.positions
    assert "AAPL" not in session.position_states
    assert "AAPL" not in session.risk_plans

    assert session.cash == 500.4
    assert session.equity == 500.4
    assert session.open_positions == 0


def run_activation_phase(
    repository: JsonTradingSessionRepository,
    iterations: int,
    interval: int,
) -> None:
    print()
    print("=========================================")
    print("PHASE 1 - ACTIVATE MANAGED TRAILING STOP")
    print("=========================================")

    runner = build_runner(
        repository=repository,
        iterations=iterations,
        interval=interval,
        price=106.0,
    )

    result = runner.run()

    persisted_session = repository.load()
    print_session("SESSION AFTER PHASE 1", persisted_session)

    assert result.iterations_completed == iterations
    assert result.failed_iterations == 0

    validate_managed_position(persisted_session)

    print()
    print("PHASE 1: PASS")


def run_recovery_exit_phase(
    repository: JsonTradingSessionRepository,
    iterations: int,
    interval: int,
) -> None:
    print()
    print("=========================================")
    print("PHASE 2 - RESTART AND EXECUTE EXIT")
    print("=========================================")

    before_restart = repository.load()
    print_session("SESSION BEFORE RESTART EXIT", before_restart)

    validate_managed_position(before_restart)

    runner = build_runner(
        repository=repository,
        iterations=iterations,
        interval=interval,
        price=100.4,
    )

    result = runner.run()

    persisted_session = repository.load()
    print_session("SESSION AFTER RESTART EXIT", persisted_session)

    assert result.iterations_completed == iterations
    assert result.failed_iterations == 0

    validate_closed_session(persisted_session)

    print()
    print("PHASE 2: PASS")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Isolated restart exit recovery smoke test."
        ),
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help=(
            "Reset the smoke session and run both phases: "
            "activate trailing stop, then restart and close."
        ),
    )
    parser.add_argument(
        "--exit-only",
        action="store_true",
        help=(
            "Use the existing smoke session and run only "
            "the restart exit phase."
        ),
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=1,
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.iterations < 1:
        raise ValueError("iterations must be at least 1.")

    if args.interval < 1:
        raise ValueError("interval must be at least 1.")

    repository = JsonTradingSessionRepository(
        path=SESSION_PATH,
    )

    if args.reset:
        repository.delete()
        repository.save(build_seed_session())
        print(f"Seeded managed session: {SESSION_PATH}")

        initial_session = repository.load()
        print_session("INITIAL SESSION", initial_session)

        run_activation_phase(
            repository=repository,
            iterations=args.iterations,
            interval=args.interval,
        )

        print()
        print(
            "Persisted lifecycle ready. "
            "A new runner instance will now load it."
        )

        run_recovery_exit_phase(
            repository=repository,
            iterations=args.iterations,
            interval=args.interval,
        )

    elif args.exit_only:
        if not repository.exists():
            raise FileNotFoundError(
                "Smoke session not found. Run with --reset first."
            )

        print(f"Restarting persisted session: {SESSION_PATH}")

        run_recovery_exit_phase(
            repository=repository,
            iterations=args.iterations,
            interval=args.interval,
        )

    else:
        repository.delete()
        repository.save(build_seed_session())
        print(f"Seeded managed session: {SESSION_PATH}")

        run_activation_phase(
            repository=repository,
            iterations=args.iterations,
            interval=args.interval,
        )

        print()
        print(
            "Phase 1 is persisted. Run again with --exit-only "
            "to execute the restart recovery exit."
        )
        return

    print()
    print("=========================================")
    print("RESTART EXIT RECOVERY: PASS")
    print("=========================================")


if __name__ == "__main__":
    main()
