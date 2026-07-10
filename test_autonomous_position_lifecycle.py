from __future__ import annotations

from pathlib import Path

from models.autonomous_paper_trading_config import AutonomousPaperTradingConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.autonomous_paper_trading_runner import AutonomousPaperTradingRunner
from services.stores.json_trading_session_repository import JsonTradingSessionRepository


class EmptyScanner:
    def run(self, session):
        return type(
            "ScanResult",
            (),
            {"candidates": [], "scanned_symbols": 0},
        )()


class FixedPriceProvider:
    def __init__(self, price: float):
        self.price = price

    def get_current_price(self, symbol: str) -> float:
        return self.price


def build_config() -> AutonomousPaperTradingConfig:
    return AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=500.0,
            take_profit_percent=0.05,
            stop_loss_percent=0.04,
        ),
    )


def build_managed_session() -> TradingSession:
    return TradingSession(
        name="Position Lifecycle Test",
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
                notes="Autonomous position lifecycle regression test.",
            ),
        },
        status="ACTIVE",
    )


def build_legacy_session() -> TradingSession:
    return TradingSession(
        name="Legacy Position Test",
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
        position_states={},
        risk_plans={},
        status="ACTIVE",
    )


def run_session(filename: str, session: TradingSession, price: float):
    repository = JsonTradingSessionRepository(
        path=Path(f"output/{filename}"),
    )
    repository.delete()
    repository.save(session)

    runner = AutonomousPaperTradingRunner(
        config=build_config(),
        scanner=EmptyScanner(),
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(price),
    )

    result = runner.run()
    assert result.failed_cycles == 0
    return repository, result


def test_runner_uses_managed_lifecycle_instead_of_fixed_take_profit():
    repository, result = run_session(
        "test_managed_lifecycle_routing.json",
        build_managed_session(),
        106.0,
    )

    assert "AAPL" in result.session.portfolio.positions
    state = result.session.position_states["AAPL"]
    assert state.current_price == 106.0
    assert state.target_1_hit is True
    assert state.target_2_hit is False
    assert state.target_3_hit is False
    assert state.break_even_active is True
    assert state.trailing_stop_active is True
    assert state.current_stop_loss > 100.0
    repository.delete()


def test_runner_executes_managed_dynamic_stop_exit():
    repository, result = run_session(
        "test_managed_dynamic_stop_exit.json",
        build_managed_session(),
        94.0,
    )

    assert "AAPL" not in result.session.portfolio.positions
    assert "AAPL" not in result.session.position_states
    assert "AAPL" not in result.session.risk_plans
    assert result.session.portfolio.cash == 494.0
    repository.delete()


def test_runner_executes_managed_final_target_exit():
    repository, result = run_session(
        "test_managed_final_target_exit.json",
        build_managed_session(),
        120.0,
    )

    assert "AAPL" not in result.session.portfolio.positions
    assert "AAPL" not in result.session.position_states
    assert "AAPL" not in result.session.risk_plans
    assert result.session.portfolio.cash == 520.0
    repository.delete()


def test_runner_uses_fixed_percentage_fallback_for_legacy_position():
    repository, result = run_session(
        "test_legacy_position_fallback.json",
        build_legacy_session(),
        106.0,
    )

    assert "AAPL" not in result.session.portfolio.positions
    assert result.session.portfolio.cash == 506.0
    assert result.session.position_states == {}
    assert result.session.risk_plans == {}

    restored = repository.load()
    assert "AAPL" not in restored.portfolio.positions
    assert restored.portfolio.cash == 506.0
    repository.delete()


def main():
    print()
    print("=========================================")
    print("AUTONOMOUS POSITION LIFECYCLE TEST")
    print("=========================================")
    print()

    test_runner_uses_managed_lifecycle_instead_of_fixed_take_profit()
    test_runner_executes_managed_dynamic_stop_exit()
    test_runner_executes_managed_final_target_exit()
    test_runner_uses_fixed_percentage_fallback_for_legacy_position()

    print("AUTONOMOUS POSITION LIFECYCLE: PASS")


if __name__ == "__main__":
    main()
