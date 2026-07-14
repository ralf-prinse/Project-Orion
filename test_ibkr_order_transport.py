from __future__ import annotations

import threading

from ibapi.contract import Contract
from ibapi.order import Order as IbkrOrder

from services.ibkr.ibkr_broker import (
    IbkrOrderOutcome,
)
from services.ibkr.ibkr_order_transport import (
    IbkrOrderTransport,
    IbkrOrderTransportError,
)


class FakeIbkrOrderClient:
    def __init__(self) -> None:
        self.connection_ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.terminal_event = threading.Event()

        self.next_order_id: int | None = None
        self.active_order_id: int | None = None

        self.managed_accounts: list[str] = []
        self.outcome: IbkrOrderOutcome | None = None
        self.errors: list[str] = []

        self.connected = False
        self.connect_called = False
        self.run_called = False
        self.disconnect_called = False
        self.managed_accounts_requested = False
        self.place_order_called = False
        self.cancel_order_called = False

        self.received_order_id: int | None = None
        self.received_contract = None
        self.received_order = None

        self.emit_connection_ready = True
        self.emit_accounts_ready = True
        self.emit_terminal_outcome = True

        self.returned_order_id = 500

        self.returned_managed_accounts = [
            "DU123456",
        ]

        self.returned_outcome = IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=1,
            average_fill_price=100.25,
            message="Filled by fake order client.",
        )

    def reset_connection_state(self) -> None:
        self.connection_ready.clear()
        self.accounts_ready.clear()

        self.next_order_id = None
        self.managed_accounts = []
        self.errors = []

    def connect(
        self,
        host: str,
        port: int,
        clientId: int,
    ) -> None:
        self.connect_called = True
        self.connected = True

    def run(self) -> None:
        self.run_called = True

        if self.emit_connection_ready:
            self.next_order_id = (
                self.returned_order_id
            )
            self.connection_ready.set()

    def isConnected(self) -> bool:
        return self.connected

    def disconnect(self) -> None:
        self.disconnect_called = True
        self.connected = False

    def reqManagedAccts(self) -> None:
        self.managed_accounts_requested = True

        if self.emit_accounts_ready:
            self.managed_accounts = list(
                self.returned_managed_accounts
            )
            self.accounts_ready.set()

    def reset_order_state(
        self,
        order_id: int,
    ) -> None:
        self.active_order_id = order_id
        self.outcome = None
        self.errors = []
        self.terminal_event.clear()

    def placeOrder(
        self,
        order_id: int,
        contract,
        order,
    ) -> None:
        self.place_order_called = True
        self.received_order_id = order_id
        self.received_contract = contract
        self.received_order = order

        if self.emit_terminal_outcome:
            self.outcome = (
                self.returned_outcome
            )
            self.terminal_event.set()

    def cancelOrder(
        self,
        order_id: int,
        manual_cancel_time: str = "",
    ) -> None:
        self.cancel_order_called = True


def create_contract() -> Contract:
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract


def create_ibkr_order() -> IbkrOrder:
    order = IbkrOrder()
    order.action = "BUY"
    order.orderType = "MKT"
    order.totalQuantity = 1
    order.transmit = True
    return order


def create_enabled_transport(
    client: FakeIbkrOrderClient,
    *,
    disconnect_after_order: bool = True,
    connection_timeout_seconds: float = 1.0,
) -> IbkrOrderTransport:
    return IbkrOrderTransport(
        paper_account_id="DU123456",
        allow_order_submission=True,
        disconnect_after_order=disconnect_after_order,
        connection_timeout_seconds=(
            connection_timeout_seconds
        ),
        client=client,
    )


def test_submission_is_disabled_by_default() -> None:
    client = FakeIbkrOrderClient()

    transport = IbkrOrderTransport(
        paper_account_id="DU123456",
        client=client,
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except PermissionError as exc:
        assert "submission is disabled" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected disabled submission to fail."
        )

    assert client.connect_called is False
    assert client.place_order_called is False


def test_submits_controlled_paper_order() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    outcome = transport.submit_order(
        contract=create_contract(),
        order=create_ibkr_order(),
        timeout_seconds=1.0,
    )

    assert outcome.status == "FILLED"
    assert outcome.filled_quantity == 1
    assert outcome.average_fill_price == 100.25

    assert client.connect_called is True
    assert client.run_called is True
    assert client.managed_accounts_requested is True
    assert client.place_order_called is True
    assert client.received_order_id == 500
    assert client.received_order.account == "DU123456"
    assert client.disconnect_called is True


def test_verifies_configured_paper_account() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client,
        disconnect_after_order=False,
    )

    transport.submit_order(
        contract=create_contract(),
        order=create_ibkr_order(),
        timeout_seconds=1.0,
    )

    assert (
        transport.verified_account_id
        == "DU123456"
    )

    transport.disconnect()


def test_rejects_missing_configured_paper_account() -> None:
    client = FakeIbkrOrderClient()

    client.returned_managed_accounts = [
        "DU999999",
    ]

    transport = create_enabled_transport(
        client
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except IbkrOrderTransportError as exc:
        assert (
            "DU123456 was not returned"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected account mismatch to fail."
        )

    assert client.place_order_called is False
    assert client.disconnect_called is True


def test_rejects_when_only_live_account_is_returned() -> None:
    client = FakeIbkrOrderClient()

    client.returned_managed_accounts = [
        "U123456",
    ]

    transport = create_enabled_transport(
        client
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except IbkrOrderTransportError as exc:
        assert (
            "DU123456 was not returned"
            in str(exc)
        )
        assert "U123456" in str(exc)
    else:
        raise AssertionError(
            "Expected live-only account response to fail."
        )

    assert client.place_order_called is False


def test_managed_accounts_timeout_blocks_order() -> None:
    client = FakeIbkrOrderClient()
    client.emit_accounts_ready = False

    transport = create_enabled_transport(
        client,
        connection_timeout_seconds=0.01,
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except IbkrOrderTransportError as exc:
        assert "managed accounts" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected managed-account timeout."
        )

    assert client.place_order_called is False
    assert client.disconnect_called is True


def test_claims_and_increments_order_id() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client,
        disconnect_after_order=False,
    )

    transport.submit_order(
        contract=create_contract(),
        order=create_ibkr_order(),
        timeout_seconds=1.0,
    )

    assert client.received_order_id == 500
    assert client.next_order_id == 501

    transport.disconnect()


def test_maps_cancelled_outcome() -> None:
    client = FakeIbkrOrderClient()

    client.returned_outcome = IbkrOrderOutcome(
        status="CANCELLED",
        message="Cancelled by fake client.",
    )

    transport = create_enabled_transport(
        client
    )

    outcome = transport.submit_order(
        contract=create_contract(),
        order=create_ibkr_order(),
        timeout_seconds=1.0,
    )

    assert outcome.status == "CANCELLED"
    assert (
        outcome.message
        == "Cancelled by fake client."
    )


def test_timeout_cancels_order() -> None:
    client = FakeIbkrOrderClient()
    client.emit_terminal_outcome = False

    transport = create_enabled_transport(
        client
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=0.01,
        )
    except TimeoutError as exc:
        assert "terminal IBKR order status" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected terminal order timeout."
        )

    assert client.cancel_order_called is True
    assert client.disconnect_called is True


def test_connection_timeout_disconnects() -> None:
    client = FakeIbkrOrderClient()
    client.emit_connection_ready = False

    transport = create_enabled_transport(
        client,
        connection_timeout_seconds=0.01,
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except IbkrOrderTransportError as exc:
        assert "connection readiness" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected connection timeout."
        )

    assert client.disconnect_called is True
    assert client.place_order_called is False


def test_rejects_live_account_id() -> None:
    client = FakeIbkrOrderClient()

    try:
        IbkrOrderTransport(
            paper_account_id="U123456",
            client=client,
        )
    except ValueError as exc:
        assert "starting with 'DU'" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected live account ID to fail."
        )


def test_rejects_non_paper_port() -> None:
    client = FakeIbkrOrderClient()

    try:
        IbkrOrderTransport(
            paper_account_id="DU123456",
            port=7496,
            client=client,
        )
    except ValueError as exc:
        assert "only TWS Paper port 7497" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected live port to fail."
        )


def test_rejects_non_stock_contract() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    contract = create_contract()
    contract.secType = "OPT"

    try:
        transport.submit_order(
            contract=contract,
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except ValueError as exc:
        assert "only STK contracts" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected non-stock contract to fail."
        )

    assert client.connect_called is False


def test_rejects_non_smart_exchange() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    contract = create_contract()
    contract.exchange = "NYSE"

    try:
        transport.submit_order(
            contract=contract,
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except ValueError as exc:
        assert "only SMART routing" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected non-SMART exchange to fail."
        )

    assert client.connect_called is False


def test_rejects_sell_order() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    order = create_ibkr_order()
    order.action = "SELL"

    try:
        transport.submit_order(
            contract=create_contract(),
            order=order,
            timeout_seconds=1.0,
        )
    except ValueError as exc:
        assert "only BUY orders" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected SELL order to fail."
        )

    assert client.connect_called is False


def test_rejects_limit_order() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    order = create_ibkr_order()
    order.orderType = "LMT"

    try:
        transport.submit_order(
            contract=create_contract(),
            order=order,
            timeout_seconds=1.0,
        )
    except ValueError as exc:
        assert "only MKT orders" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected limit order to fail."
        )

    assert client.connect_called is False


def test_rejects_zero_quantity() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    order = create_ibkr_order()
    order.totalQuantity = 0

    try:
        transport.submit_order(
            contract=create_contract(),
            order=order,
            timeout_seconds=1.0,
        )
    except ValueError as exc:
        assert "greater than zero" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected zero quantity to fail."
        )

    assert client.connect_called is False


def test_rejects_untransmitted_order() -> None:
    client = FakeIbkrOrderClient()

    transport = create_enabled_transport(
        client
    )

    order = create_ibkr_order()
    order.transmit = False

    try:
        transport.submit_order(
            contract=create_contract(),
            order=order,
            timeout_seconds=1.0,
        )
    except ValueError as exc:
        assert "transmit=True" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected untransmitted order to fail."
        )

    assert client.connect_called is False


def test_terminal_event_without_outcome_fails() -> None:
    client = FakeIbkrOrderClient()
    client.returned_outcome = None

    transport = create_enabled_transport(
        client
    )

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_ibkr_order(),
            timeout_seconds=1.0,
        )
    except IbkrOrderTransportError as exc:
        assert "without an outcome" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected missing terminal outcome to fail."
        )


def test_disconnect_is_idempotent() -> None:
    client = FakeIbkrOrderClient()

    transport = IbkrOrderTransport(
        paper_account_id="DU123456",
        client=client,
    )

    transport.disconnect()
    transport.disconnect()

    assert transport.is_connected is False
    assert transport.verified_account_id is None


def run() -> None:
    tests = [
        test_submission_is_disabled_by_default,
        test_submits_controlled_paper_order,
        test_verifies_configured_paper_account,
        test_rejects_missing_configured_paper_account,
        test_rejects_when_only_live_account_is_returned,
        test_managed_accounts_timeout_blocks_order,
        test_claims_and_increments_order_id,
        test_maps_cancelled_outcome,
        test_timeout_cancels_order,
        test_connection_timeout_disconnects,
        test_rejects_live_account_id,
        test_rejects_non_paper_port,
        test_rejects_non_stock_contract,
        test_rejects_non_smart_exchange,
        test_rejects_sell_order,
        test_rejects_limit_order,
        test_rejects_zero_quantity,
        test_rejects_untransmitted_order,
        test_terminal_event_without_outcome_fails,
        test_disconnect_is_idempotent,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR ORDER TRANSPORT TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()