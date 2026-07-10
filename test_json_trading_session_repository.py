from __future__ import annotations

from pathlib import Path

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


def test_json_trading_session_repository_roundtrip():
    repository = JsonTradingSessionRepository(
        path=Path("data/test_trading_session.json"),
    )

    repository.delete()

    paper_position = PaperPosition(
        symbol="AAPL",
        quantity=2,
        entry_price=100.0,
        current_price=105.0,
    )

    portfolio = PaperPortfolio(
        cash=800.0,
        positions={
            "AAPL": paper_position,
        },
    )

    position_state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=105.0,
        current_price=105.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=False,
        target_2_hit=False,
        target_3_hit=False,
    )

    risk_plan = RiskPlan(
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
        notes="Trading session repository regression test.",
    )

    session = TradingSession(
        name="Repository Test Session",
        portfolio=portfolio,
        position_states={
            "AAPL": position_state,
        },
        risk_plans={
            "AAPL": risk_plan,
        },
        status="ACTIVE",
    )

    repository.save(session)

    assert repository.exists() is True

    loaded = repository.load()

    assert loaded.name == "Repository Test Session"
    assert loaded.status == "ACTIVE"

    assert loaded.portfolio.cash == 800.0
    assert loaded.portfolio.equity == 1010.0
    assert loaded.portfolio.positions.keys() == {"AAPL"}

    loaded_position = loaded.portfolio.positions["AAPL"]

    assert loaded_position.symbol == "AAPL"
    assert loaded_position.quantity == 2
    assert loaded_position.entry_price == 100.0
    assert loaded_position.current_price == 105.0
    assert loaded_position.market_value == 210.0
    assert loaded_position.unrealized_profit_loss == 10.0

    assert loaded.position_states.keys() == {"AAPL"}

    loaded_state = loaded.position_states["AAPL"]

    assert loaded_state.symbol == "AAPL"
    assert loaded_state.entry_price == 100.0
    assert loaded_state.current_stop_loss == 95.0
    assert loaded_state.highest_price == 105.0
    assert loaded_state.current_price == 105.0
    assert loaded_state.break_even_active is True
    assert loaded_state.trailing_stop_active is True
    assert loaded_state.target_1_hit is False
    assert loaded_state.target_2_hit is False
    assert loaded_state.target_3_hit is False

    assert loaded.risk_plans.keys() == {"AAPL"}

    loaded_risk_plan = loaded.risk_plans["AAPL"]

    assert loaded_risk_plan.symbol == "AAPL"
    assert loaded_risk_plan.entry_price == 100.0
    assert loaded_risk_plan.stop_loss == 95.0
    assert loaded_risk_plan.target_1 == 110.0
    assert loaded_risk_plan.target_2 == 115.0
    assert loaded_risk_plan.target_3 == 120.0
    assert loaded_risk_plan.risk_percent == 5.0
    assert loaded_risk_plan.reward_percent == 10.0
    assert loaded_risk_plan.risk_reward_ratio == 2.0
    assert loaded_risk_plan.confidence == 0.90
    assert (
        loaded_risk_plan.notes
        == "Trading session repository regression test."
    )

    repository.delete()

    assert repository.exists() is False


def test_json_trading_session_repository_raises_when_missing():
    repository = JsonTradingSessionRepository(
        path=Path("data/test_missing_trading_session.json"),
    )

    repository.delete()

    try:
        repository.load()
    except FileNotFoundError as error:
        assert "Trading session not found" in str(error)
    else:
        raise AssertionError(
            "Expected FileNotFoundError for missing trading session."
        )


def main():
    print()
    print("=========================================")
    print("TRADING SESSION REPOSITORY TEST")
    print("=========================================")
    print()

    test_json_trading_session_repository_roundtrip()
    test_json_trading_session_repository_raises_when_missing()

    print("TRADING SESSION REPOSITORY: PASS")


if __name__ == "__main__":
    main()