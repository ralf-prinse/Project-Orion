from __future__ import annotations

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.exit_engine import ExitEngine
from services.position_monitor import PositionMonitorResult


def test_exit_engine_does_not_execute_hold():
    engine = ExitEngine()

    portfolio = PaperPortfolio(
        cash=100.0,
        positions={
            "TEST": PaperPosition(
                symbol="TEST",
                quantity=1,
                entry_price=100.0,
                current_price=102.0,
            )
        },
    )

    decision = PositionMonitorResult(
        symbol="TEST",
        action="HOLD",
        reason="No exit condition reached.",
        current_price=102.0,
        entry_price=100.0,
        unrealized_profit_loss=2.0,
        unrealized_return_percent=0.02,
    )

    result = engine.execute(
        portfolio=portfolio,
        decision=decision,
    )

    assert result.executed is False
    assert result.reason == "No exit execution required."
    assert portfolio.cash == 100.0
    assert "TEST" in portfolio.positions


def test_exit_engine_executes_take_profit():
    engine = ExitEngine()

    portfolio = PaperPortfolio(
        cash=100.0,
        positions={
            "TEST": PaperPosition(
                symbol="TEST",
                quantity=2,
                entry_price=100.0,
                current_price=108.0,
            )
        },
    )

    decision = PositionMonitorResult(
        symbol="TEST",
        action="TAKE_PROFIT",
        reason="Take profit threshold reached.",
        current_price=108.0,
        entry_price=100.0,
        unrealized_profit_loss=16.0,
        unrealized_return_percent=0.08,
    )

    result = engine.execute(
        portfolio=portfolio,
        decision=decision,
    )

    assert result.executed is True
    assert result.action == "TAKE_PROFIT"
    assert result.reason == "Position closed (TAKE_PROFIT)."
    assert portfolio.cash == 316.0
    assert "TEST" not in portfolio.positions


def test_exit_engine_executes_stop_loss():
    engine = ExitEngine()

    portfolio = PaperPortfolio(
        cash=100.0,
        positions={
            "TEST": PaperPosition(
                symbol="TEST",
                quantity=1,
                entry_price=100.0,
                current_price=96.0,
            )
        },
    )

    decision = PositionMonitorResult(
        symbol="TEST",
        action="STOP_LOSS",
        reason="Stop loss threshold reached.",
        current_price=96.0,
        entry_price=100.0,
        unrealized_profit_loss=-4.0,
        unrealized_return_percent=-0.04,
    )

    result = engine.execute(
        portfolio=portfolio,
        decision=decision,
    )

    assert result.executed is True
    assert result.action == "STOP_LOSS"
    assert portfolio.cash == 196.0
    assert "TEST" not in portfolio.positions


def main():
    print("\n=========================================")
    print("ORION EXIT ENGINE TEST")
    print("=========================================\n")

    test_exit_engine_does_not_execute_hold()
    test_exit_engine_executes_take_profit()
    test_exit_engine_executes_stop_loss()

    print("EXIT ENGINE: PASS ✅")


if __name__ == "__main__":
    main()