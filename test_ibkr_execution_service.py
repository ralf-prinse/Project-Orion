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
from services.ibkr.ibkr_execution_service import (
    IbkrExecutionService,
)


class FakeContextBuilder:
    def __init__(self) -> None:
        self.build_calls = 0
        self.received_request = None
        self.received_current_prices = None

    def build(
        self,
        *,
        request: ExecutionRequest,
        current_prices,
    ) -> ExecutionContext:
        self.build_calls += 1
        self.received_request = request
        self.received_current_prices = current_prices

        return ExecutionContext(
            request=request,
            portfolio=PaperPortfolio(
                cash=9723.26,
                positions={
                    "AAPL": PaperPosition(
                        symbol="AAPL",
                        quantity=1,
                        entry_price=316.58,
                        current_price=315.58,
                    )
                },
            ),
            trading_mode="PAPER",
            max_position_percentage=0.25,
            allow_fractional_shares=False,
        )


class FakeIbkrTransport:
    def __init__(self) -> None:
        self.submit_calls = 0
        self.received_contract = None
        self.received_order = None
        self.received_timeout_seconds = None

    def submit_order(
        self,
        *,
        contract,
        order,
        timeout_seconds: float,
    ) -> IbkrOrderOutcome:
        self.submit_calls += 1
        self.received_contract = contract
        self.received_order = order
        self.received_timeout_seconds = timeout_seconds

        return IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=1,
            average_fill_price=315.58,
            filled_at=datetime(
                2026,
                7,
                14,
                18,
                30,
                0,
            ),
            message="Filled by fake IBKR transport.",
        )


def create_risk_plan() -> RiskPlan:
    return RiskPlan(
        symbol="MSFT",
        entry_price=315.58,
        stop_loss=300.0,
        target_1=325.0,
        target_2=335.0,
        target_3=345.0,
        risk_percent=4.94,
        reward_percent=2.99,
        risk_reward_ratio=0.61,
        confidence=0.80,
        notes="IBKR execution service test",
    )


def create_request() -> ExecutionRequest:
    return ExecutionRequest(
        symbol="MSFT",
        action="OPEN_POSITION",
        entry_price=315.58,
        quantity=1,
        risk_plan=create_risk_plan(),
        confidence=0.80,
        strategy="DEFAULT",
        source="test_ibkr_execution_service",
    )


def create_service():
    context_builder = FakeContextBuilder()
    transport = FakeIbkrTransport()

    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=12.5,
        exchange="SMART",
        currency="USD",
    )

    execution_engine = ExecutionEngine(
        broker=broker,
    )

    service = IbkrExecutionService(
        context_builder=context_builder,
        execution_engine=execution_engine,
    )

    return service, context_builder, transport


def test_executes_request_through_existing_engine() -> None:
    service, context_builder, transport = create_service()

    request = create_request()

    current_prices = {
        "AAPL": 315.58,
    }

    result = service.execute(
        request=request,
        current_prices=current_prices,
    )

    assert context_builder.build_calls == 1
    assert context_builder.received_request is request
    assert (
        context_builder.received_current_prices
        is current_prices
    )

    assert transport.submit_calls == 1
    assert transport.received_timeout_seconds == 12.5

    contract = transport.received_contract

    assert contract is not None
    assert contract.symbol == "MSFT"
    assert contract.secType == "STK"
    assert contract.exchange == "SMART"
    assert contract.currency == "USD"

    ibkr_order = transport.received_order

    assert ibkr_order is not None
    assert ibkr_order.action == "BUY"
    assert ibkr_order.orderType == "MKT"
    assert ibkr_order.totalQuantity == 1
    assert ibkr_order.eTradeOnly is False
    assert ibkr_order.firmQuoteOnly is False
    assert ibkr_order.transmit is True

    assert result.validation.is_valid is True

    assert result.execution.accepted is True
    assert result.execution.status == "FILLED"
    assert result.execution.executed_quantity == 1
    assert result.execution.executed_price == 315.58
    assert (
        result.execution.message
        == "Filled by fake IBKR transport."
    )

    assert result.portfolio.cash == 9407.68

    assert set(result.portfolio.positions) == {
        "AAPL",
        "MSFT",
    }

    existing_position = result.portfolio.positions["AAPL"]

    assert existing_position.quantity == 1
    assert existing_position.entry_price == 316.58
    assert existing_position.current_price == 315.58

    new_position = result.portfolio.positions["MSFT"]

    assert new_position.quantity == 1
    assert new_position.entry_price == 315.58
    assert new_position.current_price == 315.58

    assert result.snapshot.equity == 10038.84
    assert result.report.status == "FILLED"


def test_returns_validation_rejection_without_transport_call() -> None:
    service, context_builder, transport = create_service()

    request = create_request()

    invalid_context = ExecutionContext(
        request=request,
        portfolio=PaperPortfolio(
            cash=100.0,
            positions={},
        ),
        trading_mode="PAPER",
        max_position_percentage=0.25,
        allow_fractional_shares=False,
    )

    def build_invalid_context(
        *,
        request,
        current_prices,
    ) -> ExecutionContext:
        context_builder.build_calls += 1
        return invalid_context

    context_builder.build = build_invalid_context

    result = service.execute(
        request=request,
        current_prices={
            "AAPL": 315.58,
        },
    )

    assert context_builder.build_calls == 1
    assert transport.submit_calls == 0

    assert result.validation.is_valid is False
    assert result.execution.accepted is False
    assert result.execution.status == "REJECTED"

    assert result.portfolio.cash == 100.0
    assert result.portfolio.positions == {}


def test_propagates_context_builder_error() -> None:
    service, context_builder, transport = create_service()

    expected_error = RuntimeError(
        "IBKR portfolio could not be read."
    )

    def failing_build(
        *,
        request,
        current_prices,
    ):
        context_builder.build_calls += 1
        raise expected_error

    context_builder.build = failing_build

    try:
        service.execute(
            request=create_request(),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except RuntimeError as exc:
        assert exc is expected_error
    else:
        raise AssertionError(
            "Expected context-builder error to propagate."
        )

    assert context_builder.build_calls == 1
    assert transport.submit_calls == 0


def run() -> None:
    tests = [
        test_executes_request_through_existing_engine,
        test_returns_validation_rejection_without_transport_call,
        test_propagates_context_builder_error,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR EXECUTION SERVICE TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()