from __future__ import annotations

from dataclasses import dataclass

from models.execution_request import ExecutionRequest
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from services.execution_request_builder import (
    ExecutionRequestBuilder,
)
from services.ibkr.ibkr_trading_service import (
    IbkrTradingService,
)


@dataclass(frozen=True)
class FakeExecutionOutput:
    accepted: bool
    status: str
    message: str


class FakeExecutionService:
    def __init__(self) -> None:
        self.calls = 0
        self.request: ExecutionRequest | None = None
        self.current_prices = None

        self.result = FakeExecutionOutput(
            accepted=True,
            status="FILLED",
            message="Filled by fake execution service.",
        )

    def execute(
        self,
        *,
        request: ExecutionRequest,
        current_prices,
    ) -> FakeExecutionOutput:
        self.calls += 1
        self.request = request
        self.current_prices = current_prices

        return self.result


def create_pipeline_result() -> TradingPipelineResult:
    risk_plan = RiskPlan(
        symbol="AAPL",
        entry_price=315.58,
        stop_loss=300.0,
        target_1=325.0,
        target_2=335.0,
        target_3=345.0,
        risk_percent=4.94,
        reward_percent=2.99,
        risk_reward_ratio=0.61,
        confidence=0.80,
        notes="IBKR trading service test",
    )

    return TradingPipelineResult(
        symbol="AAPL",
        decision="BUY",
        confidence=0.80,
        position_size=1.0,
        expected_risk=4.94,
        risk_plan=risk_plan,
        market_intelligence=None,
        ai_context=None,
        explanation="Test pipeline result.",
        investment_thesis=None,
    )


def create_service() -> tuple[
    IbkrTradingService,
    FakeExecutionService,
]:
    execution_service = FakeExecutionService()

    service = IbkrTradingService(
        request_builder=ExecutionRequestBuilder(),
        execution_service=execution_service,
    )

    return service, execution_service


def test_builds_request_and_executes_trade() -> None:
    service, execution_service = create_service()

    pipeline_result = create_pipeline_result()

    current_prices = {
        "AAPL": 315.58,
    }

    result = service.execute_trade(
        pipeline_result=pipeline_result,
        quantity=1,
        current_prices=current_prices,
    )

    assert execution_service.calls == 1
    assert execution_service.current_prices is current_prices

    request = execution_service.request

    assert request is not None
    assert request.symbol == "AAPL"
    assert request.action == "OPEN_POSITION"
    assert request.entry_price == 315.58
    assert request.quantity == 1
    assert request.risk_plan is pipeline_result.risk_plan
    assert request.confidence == 0.80
    assert request.strategy == "DEFAULT"
    assert request.source == "TradingPipeline"

    assert result is execution_service.result
    assert result.accepted is True
    assert result.status == "FILLED"


def test_passes_requested_quantity_to_builder() -> None:
    service, execution_service = create_service()

    service.execute_trade(
        pipeline_result=create_pipeline_result(),
        quantity=3,
        current_prices={
            "AAPL": 315.58,
        },
    )

    request = execution_service.request

    assert request is not None
    assert request.quantity == 3


def test_rejects_zero_quantity() -> None:
    service, execution_service = create_service()

    try:
        service.execute_trade(
            pipeline_result=create_pipeline_result(),
            quantity=0,
            current_prices={},
        )
    except ValueError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero quantity to fail."
        )

    assert execution_service.calls == 0


def test_rejects_negative_quantity() -> None:
    service, execution_service = create_service()

    try:
        service.execute_trade(
            pipeline_result=create_pipeline_result(),
            quantity=-1,
            current_prices={},
        )
    except ValueError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected negative quantity to fail."
        )

    assert execution_service.calls == 0


def test_rejects_non_integer_quantity() -> None:
    service, execution_service = create_service()

    try:
        service.execute_trade(
            pipeline_result=create_pipeline_result(),
            quantity=1.5,
            current_prices={},
        )
    except ValueError as exc:
        assert "integer" in str(exc)
    else:
        raise AssertionError(
            "Expected non-integer quantity to fail."
        )

    assert execution_service.calls == 0


def test_propagates_execution_service_error() -> None:
    service, execution_service = create_service()

    expected_error = RuntimeError(
        "Fake execution failure."
    )

    def failing_execute(
        *,
        request,
        current_prices,
    ):
        execution_service.calls += 1
        raise expected_error

    execution_service.execute = failing_execute

    try:
        service.execute_trade(
            pipeline_result=create_pipeline_result(),
            quantity=1,
            current_prices={
                "AAPL": 315.58,
            },
        )
    except RuntimeError as exc:
        assert exc is expected_error
    else:
        raise AssertionError(
            "Expected execution-service error to propagate."
        )

    assert execution_service.calls == 1


def run() -> None:
    tests = [
        test_builds_request_and_executes_trade,
        test_passes_requested_quantity_to_builder,
        test_rejects_zero_quantity,
        test_rejects_negative_quantity,
        test_rejects_non_integer_quantity,
        test_propagates_execution_service_error,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR TRADING SERVICE TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()