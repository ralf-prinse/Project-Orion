from __future__ import annotations

from models.execution_request import ExecutionRequest
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.risk_plan import RiskPlan
from services.ibkr.ibkr_execution_context_builder import (
    IbkrExecutionContextBuilder,
    IbkrExecutionContextBuilderError,
)


class FakeIbkrPortfolioService:
    def __init__(self) -> None:
        self.reads = 0
        self.received_current_prices = None

    def read_portfolio(
        self,
        *,
        current_prices,
    ) -> PaperPortfolio:
        self.reads += 1
        self.received_current_prices = current_prices

        return PaperPortfolio(
            cash=9723.26,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=1,
                    entry_price=316.58,
                    current_price=315.58,
                )
            },
        )


def create_risk_plan(
    *,
    symbol: str = "AAPL",
) -> RiskPlan:
    return RiskPlan(
        symbol=symbol,
        entry_price=315.58,
        stop_loss=300.0,
        target_1=325.0,
        target_2=335.0,
        target_3=345.0,
        risk_percent=4.94,
        reward_percent=2.99,
        risk_reward_ratio=0.61,
        confidence=0.80,
        notes="IBKR execution context builder test",
    )


def create_request(
    *,
    symbol: str = "AAPL",
    action: str = "OPEN_POSITION",
    entry_price: float = 315.58,
    quantity: int = 1,
    confidence: float = 0.80,
    risk_plan: RiskPlan | None = None,
) -> ExecutionRequest:
    return ExecutionRequest(
        symbol=symbol,
        action=action,
        entry_price=entry_price,
        quantity=quantity,
        risk_plan=(
            risk_plan
            if risk_plan is not None
            else create_risk_plan(
                symbol=symbol,
            )
        ),
        confidence=confidence,
        strategy="DEFAULT",
        source="test_ibkr_execution_context_builder",
    )


def create_builder(
    *,
    max_position_percentage: float = 0.25,
    allow_fractional_shares: bool = False,
) -> tuple[
    IbkrExecutionContextBuilder,
    FakeIbkrPortfolioService,
]:
    portfolio_service = FakeIbkrPortfolioService()

    builder = IbkrExecutionContextBuilder(
        portfolio_service=portfolio_service,
        max_position_percentage=max_position_percentage,
        allow_fractional_shares=allow_fractional_shares,
    )

    return builder, portfolio_service


def test_builds_execution_context_from_ibkr_portfolio() -> None:
    builder, portfolio_service = create_builder()

    request = create_request()

    current_prices = {
        "AAPL": 315.58,
    }

    context = builder.build(
        request=request,
        current_prices=current_prices,
    )

    assert portfolio_service.reads == 1
    assert (
        portfolio_service.received_current_prices
        is current_prices
    )

    assert context.request is request
    assert context.trading_mode == "PAPER"
    assert context.max_position_percentage == 0.25
    assert context.allow_fractional_shares is False

    assert context.portfolio.cash == 9723.26
    assert context.portfolio.equity == 10038.84

    assert "AAPL" in context.portfolio.positions

    position = context.portfolio.positions["AAPL"]

    assert position.quantity == 1
    assert position.entry_price == 316.58
    assert position.current_price == 315.58

    assert context.symbol == "AAPL"
    assert context.available_cash == 9723.26
    assert context.portfolio_equity == 10038.84
    assert context.requested_value == 315.58
    assert context.position_size_percent == 0.0314


def test_passes_fractional_share_configuration() -> None:
    builder, _ = create_builder(
        allow_fractional_shares=True,
    )

    context = builder.build(
        request=create_request(),
        current_prices={
            "AAPL": 315.58,
        },
    )

    assert context.allow_fractional_shares is True


def test_rejects_empty_symbol() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                symbol="   ",
                risk_plan=create_risk_plan(
                    symbol="AAPL",
                ),
            ),
            current_prices={},
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "symbol must not be empty" in str(exc)
    else:
        raise AssertionError(
            "Expected empty symbol to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_unsupported_action() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                action="CLOSE_POSITION",
            ),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "only OPEN_POSITION" in str(exc)
    else:
        raise AssertionError(
            "Expected unsupported action to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_zero_quantity() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                quantity=0,
            ),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero quantity to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_non_integer_quantity() -> None:
    builder, portfolio_service = create_builder()

    request = create_request()

    object.__setattr__(
        request,
        "quantity",
        1.5,
    )

    try:
        builder.build(
            request=request,
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "must be an integer" in str(exc)
    else:
        raise AssertionError(
            "Expected non-integer quantity to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_zero_entry_price() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                entry_price=0.0,
            ),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "entry price" in str(exc)
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero entry price to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_non_finite_entry_price() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                entry_price=float("nan"),
            ),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "entry price" in str(exc)
        assert "finite" in str(exc)
    else:
        raise AssertionError(
            "Expected non-finite entry price to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_invalid_confidence() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                confidence=1.1,
            ),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "confidence" in str(exc)
        assert "between 0 and 1" in str(exc)
    else:
        raise AssertionError(
            "Expected invalid confidence to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_risk_plan_symbol_mismatch() -> None:
    builder, portfolio_service = create_builder()

    try:
        builder.build(
            request=create_request(
                symbol="AAPL",
                risk_plan=create_risk_plan(
                    symbol="MSFT",
                ),
            ),
            current_prices={
                "AAPL": 315.58,
            },
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "RiskPlan symbol must match" in str(exc)
    else:
        raise AssertionError(
            "Expected symbol mismatch to fail."
        )

    assert portfolio_service.reads == 0


def test_rejects_zero_max_position_percentage() -> None:
    portfolio_service = FakeIbkrPortfolioService()

    try:
        IbkrExecutionContextBuilder(
            portfolio_service=portfolio_service,
            max_position_percentage=0.0,
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero max-position percentage to fail."
        )


def test_rejects_max_position_percentage_above_one() -> None:
    portfolio_service = FakeIbkrPortfolioService()

    try:
        IbkrExecutionContextBuilder(
            portfolio_service=portfolio_service,
            max_position_percentage=1.1,
        )
    except IbkrExecutionContextBuilderError as exc:
        assert "at most 1" in str(exc)
    else:
        raise AssertionError(
            "Expected max-position percentage above one to fail."
        )


def run() -> None:
    tests = [
        test_builds_execution_context_from_ibkr_portfolio,
        test_passes_fractional_share_configuration,
        test_rejects_empty_symbol,
        test_rejects_unsupported_action,
        test_rejects_zero_quantity,
        test_rejects_non_integer_quantity,
        test_rejects_zero_entry_price,
        test_rejects_non_finite_entry_price,
        test_rejects_invalid_confidence,
        test_rejects_risk_plan_symbol_mismatch,
        test_rejects_zero_max_position_percentage,
        test_rejects_max_position_percentage_above_one,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR EXECUTION CONTEXT BUILDER TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()