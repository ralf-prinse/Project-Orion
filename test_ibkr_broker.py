from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime

from models.order import Order
from services.ibkr.ibkr_broker import (
    IbkrBroker,
    IbkrOrderOutcome,
)


class FakeIbkrBrokerTransport:
    def __init__(
        self,
        *,
        outcome: IbkrOrderOutcome | None = None,
        error: Exception | None = None,
    ) -> None:
        self.outcome = outcome or IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=2,
            average_fill_price=101.25,
            filled_at=datetime(2026, 7, 14, 15, 0, 0),
            message="Filled by fake transport.",
        )
        self.error = error

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

        if self.error is not None:
            raise self.error

        return self.outcome


def create_order(
    *,
    symbol: str = "AAPL",
    side: str = "BUY",
    quantity: int = 2,
    order_type: str = "MARKET",
    price: float = 100.0,
) -> Order:
    return Order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        order_type=order_type,
        price=price,
        created_at=datetime(2026, 7, 14, 14, 0, 0),
        source="test_ibkr_broker",
    )


def test_maps_complete_fill_to_execution_result() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=12.5,
    )

    original_order = create_order()

    result = broker.execute(original_order)

    assert result.accepted is True
    assert result.status == "FILLED"
    assert result.order is original_order
    assert result.message == "Filled by fake transport."
    assert result.executed_price == 101.25
    assert result.executed_quantity == 2
    assert result.executed_at == datetime(
        2026,
        7,
        14,
        15,
        0,
        0,
    )

    assert transport.submit_called is True
    assert transport.received_timeout_seconds == 12.5


def test_maps_stock_contract() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
        exchange="smart",
        currency="usd",
    )

    broker.execute(
        create_order(
            symbol=" aapl ",
        )
    )

    contract = transport.received_contract

    assert contract is not None
    assert contract.symbol == "AAPL"
    assert contract.secType == "STK"
    assert contract.exchange == "SMART"
    assert contract.currency == "USD"


def test_maps_market_buy_order() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    broker.execute(
        create_order(
            side=" buy ",
            quantity=3,
            order_type=" market ",
        )
    )

    ibkr_order = transport.received_order

    assert ibkr_order is not None
    assert ibkr_order.action == "BUY"
    assert ibkr_order.orderType == "MKT"
    assert ibkr_order.totalQuantity == 3
    assert ibkr_order.transmit is True


def test_rejects_empty_symbol_before_transport() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            symbol="   ",
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert "symbol" in result.message.lower()
    assert transport.submit_called is False


def test_maps_market_sell_order() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            side=" sell ",
            quantity=2,
            order_type=" market ",
        )
    )

    ibkr_order = transport.received_order

    assert result.accepted is True
    assert result.status == "FILLED"

    assert transport.submit_called is True
    assert ibkr_order is not None
    assert ibkr_order.action == "SELL"
    assert ibkr_order.orderType == "MKT"
    assert ibkr_order.totalQuantity == 2
    assert ibkr_order.transmit is True


def test_rejects_unsupported_order_type_before_transport() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            order_type="LIMIT",
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert "only MARKET" in result.message
    assert transport.submit_called is False


def test_rejects_zero_quantity_before_transport() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            quantity=0,
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert "greater than zero" in result.message
    assert transport.submit_called is False


def test_rejects_negative_quantity_before_transport() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            quantity=-1,
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert "greater than zero" in result.message
    assert transport.submit_called is False


def test_rejects_non_finite_price_before_transport() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            price=float("nan"),
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert "finite" in result.message
    assert transport.submit_called is False


def test_rejects_zero_price_before_transport() -> None:
    transport = FakeIbkrBrokerTransport()

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            price=0.0,
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert "greater than zero" in result.message
    assert transport.submit_called is False


def test_maps_rejected_outcome() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="REJECTED",
            message="Order rejected by broker.",
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order()
    )

    assert result.accepted is False
    assert result.status == "REJECTED"
    assert result.message == "Order rejected by broker."
    assert result.executed_quantity == 0
    assert result.executed_price == 0.0


def test_maps_cancelled_outcome() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="CANCELLED",
            message="Order cancelled.",
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order()
    )

    assert result.accepted is False
    assert result.status == "CANCELLED"
    assert result.message == "Order cancelled."


def test_rejects_partial_fill() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=1,
            average_fill_price=100.5,
            filled_at=datetime(2026, 7, 14, 15, 0, 0),
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            quantity=2,
        )
    )

    assert result.accepted is False
    assert result.status == "PARTIAL_FILL"
    assert "Expected 2" in result.message
    assert "received 1" in result.message


def test_rejects_zero_quantity_fill() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=0,
            average_fill_price=100.5,
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order(
            quantity=0,
        )
    )

    assert result.accepted is False
    assert result.status == "REJECTED"


def test_rejects_non_finite_fill_price() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=2,
            average_fill_price=float("inf"),
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order()
    )

    assert result.accepted is False
    assert result.status == "ERROR"
    assert "non-finite fill price" in result.message


def test_rejects_negative_fill_price() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=2,
            average_fill_price=-1.0,
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order()
    )

    assert result.accepted is False
    assert result.status == "ERROR"
    assert "invalid fill price" in result.message


def test_maps_transport_timeout() -> None:
    transport = FakeIbkrBrokerTransport(
        error=TimeoutError(
            "Timed out waiting for IBKR fill."
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    original_order = create_order()

    result = broker.execute(original_order)

    assert result.accepted is False
    assert result.status == "TIMEOUT"
    assert result.order is original_order
    assert result.message == "Timed out waiting for IBKR fill."


def test_maps_transport_exception() -> None:
    transport = FakeIbkrBrokerTransport(
        error=RuntimeError(
            "Transport unavailable."
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order()
    )

    assert result.accepted is False
    assert result.status == "ERROR"
    assert "Transport unavailable" in result.message


def test_uses_default_fill_timestamp_when_missing() -> None:
    transport = FakeIbkrBrokerTransport(
        outcome=IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=2,
            average_fill_price=100.5,
            filled_at=None,
        )
    )

    broker = IbkrBroker(
        transport=transport,
    )

    result = broker.execute(
        create_order()
    )

    assert result.accepted is True
    assert result.executed_at is not None


def test_order_outcome_is_immutable() -> None:
    outcome = IbkrOrderOutcome(
        status="FILLED",
    )

    try:
        outcome.status = "REJECTED"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError(
            "IbkrOrderOutcome must be immutable."
        )


def test_rejects_invalid_timeout_configuration() -> None:
    transport = FakeIbkrBrokerTransport()

    try:
        IbkrBroker(
            transport=transport,
            timeout_seconds=0,
        )
    except ValueError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected invalid timeout to fail."
        )


def test_rejects_empty_exchange_configuration() -> None:
    transport = FakeIbkrBrokerTransport()

    try:
        IbkrBroker(
            transport=transport,
            exchange="   ",
        )
    except ValueError as exc:
        assert "exchange" in str(exc).lower()
    else:
        raise AssertionError(
            "Expected empty exchange to fail."
        )


def test_rejects_empty_currency_configuration() -> None:
    transport = FakeIbkrBrokerTransport()

    try:
        IbkrBroker(
            transport=transport,
            currency="   ",
        )
    except ValueError as exc:
        assert "currency" in str(exc).lower()
    else:
        raise AssertionError(
            "Expected empty currency to fail."
        )


def run() -> None:
    tests = [
        test_maps_complete_fill_to_execution_result,
        test_maps_stock_contract,
        test_maps_market_buy_order,
        test_rejects_empty_symbol_before_transport,
        test_maps_market_sell_order,
        test_rejects_unsupported_order_type_before_transport,
        test_rejects_zero_quantity_before_transport,
        test_rejects_negative_quantity_before_transport,
        test_rejects_non_finite_price_before_transport,
        test_rejects_zero_price_before_transport,
        test_maps_rejected_outcome,
        test_maps_cancelled_outcome,
        test_rejects_partial_fill,
        test_rejects_zero_quantity_fill,
        test_rejects_non_finite_fill_price,
        test_rejects_negative_fill_price,
        test_maps_transport_timeout,
        test_maps_transport_exception,
        test_uses_default_fill_timestamp_when_missing,
        test_order_outcome_is_immutable,
        test_rejects_invalid_timeout_configuration,
        test_rejects_empty_exchange_configuration,
        test_rejects_empty_currency_configuration,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR BROKER TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()