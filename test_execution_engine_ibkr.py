from __future__ import annotations

from datetime import datetime

from models.execution_context import ExecutionContext
from models.execution_request import ExecutionRequest
from models.paper_portfolio import PaperPortfolio
from models.risk_plan import RiskPlan
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_broker import (
    IbkrBroker,
    IbkrOrderOutcome,
)


class FakeIbkrExecutionTransport:
    """
    Test double for the technical IBKR transport.

    No connection with TWS is made and no broker order is submitted.
    """

    def __init__(self) -> None:
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
            filled_quantity=2,
            average_fill_price=100.0,
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


def create_context() -> ExecutionContext:
    plan = RiskPlan(
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

    request = ExecutionRequest(
        symbol="AAPL",
        action="OPEN_POSITION",
        entry_price=100.0,
        quantity=2,
        risk_plan=plan,
        confidence=0.90,
    )

    return ExecutionContext(
        request=request,
        portfolio=PaperPortfolio(
            cash=1000.0,
        ),
        max_position_percentage=0.50,
    )


def test_execution_engine_uses_ibkr_broker_interface() -> None:
    transport = FakeIbkrExecutionTransport()

    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=12.5,
        exchange="SMART",
        currency="USD",
    )

    engine = ExecutionEngine(
        broker=broker,
    )

    result = engine.execute(
        create_context()
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
    assert (
        result.execution.message
        == "Filled by fake IBKR transport."
    )

    assert result.portfolio.cash == 800.0
    assert "AAPL" in result.portfolio.positions

    position = result.portfolio.positions["AAPL"]

    assert position.quantity == 2
    assert position.entry_price == 100.0
    assert position.current_price == 100.0

    assert result.snapshot.equity == 1000.0
    assert result.report.status == "FILLED"


def run() -> None:
    test_execution_engine_uses_ibkr_broker_interface()

    print(
        "PASS: "
        "test_execution_engine_uses_ibkr_broker_interface"
    )
    print()
    print(
        "EXECUTION ENGINE IBKR TESTS: 1 passed"
    )


if __name__ == "__main__":
    run()