from __future__ import annotations

from datetime import datetime

from models.execution_result import ExecutionResult
from models.order import Order
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.portfolio_manager import PortfolioManager


def create_execution_result(
    *,
    symbol: str = "AAPL",
    side: str,
    quantity: int,
    price: float,
) -> ExecutionResult:
    order = Order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        order_type="MARKET",
        price=price,
        created_at=datetime.now(),
        source="test_portfolio_manager",
    )

    return ExecutionResult(
        accepted=True,
        status="FILLED",
        order=order,
        message="Test order filled.",
        executed_price=price,
        executed_quantity=quantity,
        executed_at=datetime.now(),
    )


def test_applies_buy_execution() -> None:
    manager = PortfolioManager()

    portfolio = PaperPortfolio(
        cash=1000.0,
    )

    result = create_execution_result(
        side="BUY",
        quantity=2,
        price=100.0,
    )

    updated = manager.apply_execution(
        portfolio=portfolio,
        result=result,
    )

    snapshot = manager.snapshot(updated)

    assert updated.cash == 800.0
    assert "AAPL" in updated.positions
    assert updated.positions["AAPL"].quantity == 2

    assert snapshot.cash == 800.0
    assert snapshot.positions_value == 200.0
    assert snapshot.equity == 1000.0
    assert snapshot.open_positions == 1


def test_applies_complete_sell_execution() -> None:
    manager = PortfolioManager()

    portfolio = PaperPortfolio(
        cash=800.0,
        positions={
            "AAPL": PaperPosition(
                symbol="AAPL",
                quantity=2,
                entry_price=100.0,
                current_price=110.0,
            ),
        },
    )

    result = create_execution_result(
        side="SELL",
        quantity=2,
        price=110.0,
    )

    updated = manager.apply_execution(
        portfolio=portfolio,
        result=result,
    )

    snapshot = manager.snapshot(updated)

    assert updated.cash == 1020.0
    assert "AAPL" not in updated.positions

    assert snapshot.cash == 1020.0
    assert snapshot.positions_value == 0.0
    assert snapshot.equity == 1020.0
    assert snapshot.open_positions == 0


def test_applies_partial_sell_execution() -> None:
    manager = PortfolioManager()

    portfolio = PaperPortfolio(
        cash=500.0,
        positions={
            "AAPL": PaperPosition(
                symbol="AAPL",
                quantity=5,
                entry_price=100.0,
                current_price=110.0,
            ),
        },
    )

    result = create_execution_result(
        side="SELL",
        quantity=2,
        price=110.0,
    )

    updated = manager.apply_execution(
        portfolio=portfolio,
        result=result,
    )

    snapshot = manager.snapshot(updated)

    assert updated.cash == 720.0
    assert "AAPL" in updated.positions

    position = updated.positions["AAPL"]

    assert position.quantity == 3
    assert position.entry_price == 100.0
    assert position.current_price == 110.0

    assert snapshot.cash == 720.0
    assert snapshot.positions_value == 330.0
    assert snapshot.equity == 1050.0
    assert snapshot.open_positions == 1


def run() -> None:
    tests = [
        test_applies_buy_execution,
        test_applies_complete_sell_execution,
        test_applies_partial_sell_execution,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        f"PORTFOLIO MANAGER TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()