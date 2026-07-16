from __future__ import annotations

from datetime import datetime

from models.execution_context import ExecutionContext
from models.execution_request import ExecutionRequest
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.risk_plan import RiskPlan
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_broker import (
    IbkrBroker,
    IbkrOrderOutcome,
)


class FakeIbkrExecutionTransport:
    """
    Test double for the technical IBKR transport.

    No connection with TWS is made and no real broker order is submitted.
    """

    def __init__(
        self,
        *,
        filled_quantity: int = 2,
        average_fill_price: float = 100.0,
    ) -> None:
        self.filled_quantity = filled_quantity
        self.average_fill_price = average_fill_price

        self.submit_called = False
        self.received_contract = None
        self.received_order = None
        self.received_timeout_seconds: float | None = None

    def submit_order(
        self,
        *,
        contract,
        order,
        timeout_seconds: float,
    ) -> IbkrOrderOutcome:
        self.submit_called = True
        self.received_contract = contract
        self.received_order = order
        self.received_timeout_seconds = timeout_seconds

        return IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=self.filled_quantity,
            average_fill_price=self.average_fill_price,
            filled_at=datetime(
                2026,
                7,
                14,
                18,
                0,
                0,
            ),
            message="Filled by fake IBKR transport.",
        )


def create_risk_plan() -> RiskPlan:
    return RiskPlan(
        symbol="AAPL",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        target_3=130.0,
        risk_percent=5.0,
        reward_percent=10.0,
        risk_reward_ratio=2.0,
        confidence=0.90,
        notes="IBKR execution-engine integration test",
    )


def create_buy_context() -> ExecutionContext:
    request = ExecutionRequest(
        symbol="AAPL",
        action="OPEN_POSITION",
        entry_price=100.0,
        quantity=2,
        risk_plan=create_risk_plan(),
        confidence=0.90,
    )

    return ExecutionContext(
        request=request,
        portfolio=PaperPortfolio(
            cash=1000.0,
        ),
        max_position_percentage=0.50,
    )


def create_sell_context(
    *,
    quantity: int = 2,
) -> ExecutionContext:
    request = ExecutionRequest(
        symbol="AAPL",
        action="CLOSE_POSITION",
        entry_price=110.0,
        quantity=quantity,
        risk_plan=create_risk_plan(),
        confidence=0.90,
    )

    return ExecutionContext(
        request=request,
        portfolio=PaperPortfolio(
            cash=800.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=2,
                    entry_price=100.0,
                    current_price=110.0,
                ),
            },
        ),
        max_position_percentage=0.50,
    )


def create_engine(
    transport: FakeIbkrExecutionTransport,
) -> ExecutionEngine:
    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=12.5,
        exchange="SMART",
        currency="USD",
    )

    return ExecutionEngine(
        broker=broker,
    )


def test_execution_engine_uses_ibkr_broker_for_buy() -> None:
    transport = FakeIbkrExecutionTransport(
        filled_quantity=2,
        average_fill_price=100.0,
    )

    engine = create_engine(transport)

    result = engine.execute(
        create_buy_context()
    )

    assert transport.submit_called is True
    assert transport.received_timeout_seconds == 12.5

    contract = transport.received_contract

    assert contract is not None
    assert contract.symbol == "AAPL"
    assert contract.secType == "STK"
    assert contract.exchange == "SMART"
    assert contract.currency == "USD"

    ibkr_order = transport.received_order

    assert ibkr_order is not None
    assert ibkr_order.action == "BUY"
    assert ibkr_order.orderType == "MKT"
    assert ibkr_order.totalQuantity == 2
    assert ibkr_order.eTradeOnly is False
    assert ibkr_order.firmQuoteOnly is False
    assert ibkr_order.transmit is True

    assert result.validation.is_valid is True

    assert result.execution.accepted is True
    assert result.execution.status == "FILLED"
    assert result.execution.executed_quantity == 2
    assert result.execution.executed_price == 100.0

    assert result.portfolio.cash == 800.0
    assert "AAPL" in result.portfolio.positions

    position = result.portfolio.positions["AAPL"]

    assert position.quantity == 2
    assert position.entry_price == 100.0
    assert position.current_price == 100.0

    assert result.snapshot.equity == 1000.0
    assert result.report.status == "FILLED"


def test_execution_engine_uses_ibkr_broker_for_sell() -> None:
    transport = FakeIbkrExecutionTransport(
        filled_quantity=2,
        average_fill_price=110.0,
    )

    engine = create_engine(transport)

    result = engine.execute(
        create_sell_context()
    )

    assert transport.submit_called is True
    assert transport.received_timeout_seconds == 12.5

    contract = transport.received_contract

    assert contract is not None
    assert contract.symbol == "AAPL"
    assert contract.secType == "STK"
    assert contract.exchange == "SMART"
    assert contract.currency == "USD"

    ibkr_order = transport.received_order

    assert ibkr_order is not None
    assert ibkr_order.action == "SELL"
    assert ibkr_order.orderType == "MKT"
    assert ibkr_order.totalQuantity == 2
    assert ibkr_order.eTradeOnly is False
    assert ibkr_order.firmQuoteOnly is False
    assert ibkr_order.transmit is True

    assert result.validation.is_valid is True

    assert result.execution.accepted is True
    assert result.execution.status == "FILLED"
    assert result.execution.executed_quantity == 2
    assert result.execution.executed_price == 110.0

    assert result.portfolio.cash == 1020.0
    assert "AAPL" not in result.portfolio.positions

    assert result.snapshot.cash == 1020.0
    assert result.snapshot.open_positions == 0
    assert result.snapshot.positions_value == 0.0
    assert result.snapshot.equity == 1020.0

    assert result.report.status == "FILLED"


def test_execution_engine_rejects_sell_larger_than_position() -> None:
    transport = FakeIbkrExecutionTransport(
        filled_quantity=3,
        average_fill_price=110.0,
    )

    engine = create_engine(transport)

    result = engine.execute(
        create_sell_context(
            quantity=3,
        )
    )

    assert result.validation.is_valid is False
    assert result.execution.accepted is False
    assert result.execution.status == "REJECTED"

    assert transport.submit_called is False

    assert result.portfolio.cash == 800.0
    assert "AAPL" in result.portfolio.positions
    assert result.portfolio.positions["AAPL"].quantity == 2


def run() -> None:
    tests = [
        test_execution_engine_uses_ibkr_broker_for_buy,
        test_execution_engine_uses_ibkr_broker_for_sell,
        test_execution_engine_rejects_sell_larger_than_position,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        f"EXECUTION ENGINE IBKR TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()