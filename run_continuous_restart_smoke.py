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
        name="Orion Continuous Restart Smoke Test",
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
                notes="Continuous runner restart smoke test.",
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


def validate_managed_session(
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
    assert state.current_stop_loss > 100.0
    assert plan.target_3 == 120.0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Isolated restart-safe continuous runner smoke test."
        ),
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the smoke session and seed a fresh managed session.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--price",
        type=float,
        default=106.0,
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

    if not repository.exists():
        repository.save(build_seed_session())
        print(f"Seeded managed session: {SESSION_PATH}")
    else:
        print(f"Restarting persisted session: {SESSION_PATH}")

    initial_session = repository.load()
    print_session("SESSION BEFORE RUN", initial_session)

    runner = build_runner(
        repository=repository,
        iterations=args.iterations,
        interval=args.interval,
        price=args.price,
    )

    result = runner.run()

    persisted_session = repository.load()

    print_session("SESSION AFTER RUN", persisted_session)

    print()
    print("CONTINUOUS RESULT")
    print("-----------------")
    print(f"Iterations completed: {result.iterations_completed}")
    print(f"Failed iterations:    {result.failed_iterations}")

    validate_managed_session(persisted_session)

    assert result.iterations_completed == args.iterations
    assert result.failed_iterations == 0

    print()
    print("RESTART-SAFE MANAGED LIFECYCLE: PASS")


if __name__ == "__main__":
    main()
