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
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
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


def build_config(
    initial_cash: float = 500.0,
) -> AutonomousPaperTradingConfig:
    return AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=initial_cash,
        ),
    )


def build_complete_session() -> TradingSession:
    return TradingSession(
        name="Persistent Lifecycle Test",
        portfolio=PaperPortfolio(
            cash=400.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=1,
                    entry_price=100.0,
                    current_price=105.0,
                ),
            },
        ),
        position_states={
            "AAPL": PositionState(
                symbol="AAPL",
                entry_price=100.0,
                current_stop_loss=95.0,
                highest_price=108.0,
                current_price=105.0,
                break_even_active=True,
                trailing_stop_active=True,
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
                target_1=110.0,
                target_2=115.0,
                target_3=120.0,
                risk_percent=5.0,
                reward_percent=10.0,
                risk_reward_ratio=2.0,
                confidence=0.90,
                notes="Persistent lifecycle regression test.",
            ),
        },
        status="ACTIVE",
        peak_portfolio_value=550.0,
    )


def test_runner_loads_existing_portfolio():
    repository = JsonPaperPortfolioRepository(
        path="output/test_runner_portfolio.json",
    )

    repository.delete()

    repository.save(
        PaperPortfolio(
            cash=321.0,
        )
    )

    runner = AutonomousPaperTradingRunner(
        config=build_config(initial_cash=500.0),
        scanner=EmptyScanner(),
        portfolio_repository=repository,
    )

    result = runner.run()

    assert result.initial_cash == 500.0
    assert result.final_cash == 321.0
    assert result.final_equity == 321.0

    repository.delete()


def test_runner_saves_created_portfolio():
    repository = JsonPaperPortfolioRepository(
        path="output/test_runner_created_portfolio.json",
    )

    repository.delete()

    runner = AutonomousPaperTradingRunner(
        config=build_config(initial_cash=777.0),
        scanner=EmptyScanner(),
        portfolio_repository=repository,
    )

    result = runner.run()

    assert result.final_cash == 777.0
    assert repository.exists()

    restored = repository.load()

    assert restored.cash == 777.0

    repository.delete()


def test_runner_loads_complete_trading_session():
    repository = JsonTradingSessionRepository(
        path=Path("output/test_runner_trading_session.json"),
    )

    repository.delete()
    repository.save(build_complete_session())

    runner = AutonomousPaperTradingRunner(
        config=build_config(),
        scanner=EmptyScanner(),
        trading_session_repository=repository,
        price_provider=FixedPriceProvider(105.0),
    )

    result = runner.run()

    assert result.session.name == "Persistent Lifecycle Test"
    assert result.session.status == "ACTIVE"
    assert result.session.portfolio.cash == 400.0
    assert result.session.peak_portfolio_value == 550.0

    assert "AAPL" in result.session.position_states
    assert result.session.position_states["AAPL"].highest_price == 108.0
    assert result.session.position_states["AAPL"].break_even_active is True
    assert result.session.position_states["AAPL"].trailing_stop_active is True

    assert "AAPL" in result.session.risk_plans
    assert result.session.risk_plans["AAPL"].stop_loss == 95.0
    assert result.session.risk_plans["AAPL"].target_3 == 120.0

    repository.delete()


def test_runner_saves_complete_trading_session():
    repository = JsonTradingSessionRepository(
        path=Path("output/test_runner_saved_session.json"),
    )

    repository.delete()

    runner = AutonomousPaperTradingRunner(
        config=build_config(initial_cash=600.0),
        scanner=EmptyScanner(),
        trading_session_repository=repository,
    )

    result = runner.run()

    assert repository.exists() is True

    restored = repository.load()

    assert restored.name == result.session.name
    assert restored.status == result.session.status
    assert restored.portfolio.cash == 600.0
    assert restored.position_states == {}
    assert restored.risk_plans == {}
    assert restored.peak_portfolio_value == 600.0

    repository.delete()


def main():
    print()
    print("=========================================")
    print("AUTONOMOUS RUNNER PERSISTENCE TEST")
    print("=========================================")
    print()

    test_runner_loads_existing_portfolio()
    test_runner_saves_created_portfolio()
    test_runner_loads_complete_trading_session()
    test_runner_saves_complete_trading_session()

    print("AUTONOMOUS RUNNER PERSISTENCE: PASS")


if __name__ == "__main__":
    main()
