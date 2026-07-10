from __future__ import annotations

from pathlib import Path

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


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
        self.price = price

    def get_current_price(self, symbol: str) -> float:
        return self.price


def build_config() -> AutonomousPaperTradingConfig:
    return AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=500.0,
        ),
    )


def build_session() -> TradingSession:
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
                reward_percent=4.0,
                risk_reward_ratio=0.8,
                confidence=0.90,
                notes="Autonomous position lifecycle regression test.",
            ),
        },
        status="ACTIVE",
    )


def test_runner_updates_and_persists_position_lifecycle():
    repository = JsonTradingSessionRepository(
        path=Path("output/test_autonomous_position_lifecycle.json"),
    )

    repository.delete()
    repository.save(build_session())

    runner = AutonomousPaperTradingRunner(
        config=build_config(),
        scanner=EmptyScanner(),
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(106.0),
    )

    result = runner.run()

    assert "AAPL" in result.session.portfolio.positions
    assert result.session.portfolio.positions["AAPL"].current_price == 106.0

    state = result.session.position_states["AAPL"]

    assert state.current_price == 106.0
    assert state.highest_price == 106.0
    assert state.target_1_hit is True
    assert state.break_even_active is True
    assert state.trailing_stop_active is True
    assert state.current_stop_loss > 100.0

    restored = repository.load()
    restored_state = restored.position_states["AAPL"]

    assert restored.portfolio.positions["AAPL"].current_price == 106.0
    assert restored_state.current_price == 106.0
    assert restored_state.highest_price == 106.0
    assert restored_state.target_1_hit is True
    assert restored_state.break_even_active is True
    assert restored_state.trailing_stop_active is True
    assert restored_state.current_stop_loss > 100.0

    repository.delete()


def main():
    print()
    print("=========================================")
    print("AUTONOMOUS POSITION LIFECYCLE TEST")
    print("=========================================")
    print()

    test_runner_updates_and_persists_position_lifecycle()

    print("AUTONOMOUS POSITION LIFECYCLE: PASS")


if __name__ == "__main__":
    main()