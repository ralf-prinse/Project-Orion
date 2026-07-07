from datetime import datetime

from models.execution_result import ExecutionResult
from models.order import Order
from models.paper_portfolio import PaperPortfolio
from services.portfolio_manager import PortfolioManager


def run():
    manager = PortfolioManager()

    portfolio = PaperPortfolio(
        cash=1000.0,
    )

    order = Order(
        symbol="AAPL",
        side="BUY",
        quantity=2,
        order_type="MARKET",
        price=100.0,
        created_at=datetime.now(),
    )

    result = ExecutionResult(
        accepted=True,
        status="FILLED",
        order=order,
        message="Paper order filled.",
        executed_price=100.0,
        executed_quantity=2,
        executed_at=datetime.now(),
    )

    updated = manager.apply_execution(
        portfolio=portfolio,
        result=result,
    )

    snapshot = manager.snapshot(updated)

    print(updated)
    print(snapshot)

    assert updated.cash == 800.0
    assert "AAPL" in updated.positions
    assert updated.positions["AAPL"].quantity == 2

    assert snapshot.cash == 800.0
    assert snapshot.positions_value == 200.0
    assert snapshot.equity == 1000.0
    assert snapshot.open_positions == 1

    print("PASS")


if __name__ == "__main__":
    run()