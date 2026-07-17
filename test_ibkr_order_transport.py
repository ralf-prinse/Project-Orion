from __future__ import annotations

import threading
from dataclasses import dataclass

from ibapi.contract import Contract
from ibapi.order import Order as IbkrOrder

from services.ibkr.ibkr_broker import IbkrOrderOutcome
from services.ibkr.ibkr_order_transport import (
    IbkrOrderTransport,
    IbkrOrderTransportError,
)


@dataclass
class FakeExecution:
    orderId: int
    execId: str
    shares: float
    price: float
    time: str = "20260714 17:16:14"


class FakeIbkrOrderClient:
    EXECUTION_RECONCILIATION_REQUEST_ID = 9101

    def __init__(self) -> None:
        self.connection_ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.terminal_event = threading.Event()
        self.execution_reconciliation_ready = threading.Event()
        self.next_order_id: int | None = None
        self.active_order_id: int | None = None
        self.expected_quantity = 0
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
        self.executions_requested = False
        self.received_order_id: int | None = None
        self.received_order = None
        self.emit_connection_ready = True
        self.emit_accounts_ready = True
        self.emit_terminal_outcome = True
        self.emit_reconciled_execution = False
        self.returned_order_id = 500
        self.returned_managed_accounts = ["DU123456"]
        self.returned_outcome = IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=1,
            average_fill_price=100.25,
            message="Filled by fake order client.",
        )

    def reset_connection_state(self) -> None:
        self.connection_ready.clear()
        self.accounts_ready.clear()
        self.execution_reconciliation_ready.clear()
        self.next_order_id = None
        self.managed_accounts = []
        self.errors = []

    def connect(self, host: str, port: int, clientId: int) -> None:
        self.connect_called = True
        self.connected = True

    def run(self) -> None:
        self.run_called = True
        if self.emit_connection_ready:
            self.next_order_id = self.returned_order_id
            self.connection_ready.set()

    def isConnected(self) -> bool:
        return self.connected

    def disconnect(self) -> None:
        self.disconnect_called = True
        self.connected = False

    def reqManagedAccts(self) -> None:
        self.managed_accounts_requested = True
        if self.emit_accounts_ready:
            self.managed_accounts = list(self.returned_managed_accounts)
            self.accounts_ready.set()

    def reset_order_state(self, order_id: int, expected_quantity: int) -> None:
        self.active_order_id = order_id
        self.expected_quantity = expected_quantity
        self.outcome = None
        self.errors = []
        self.terminal_event.clear()
        self.execution_reconciliation_ready.clear()

    def placeOrder(self, order_id: int, contract, order) -> None:
        self.place_order_called = True
        self.received_order_id = order_id
        self.received_order = order
        if self.emit_terminal_outcome:
            self.outcome = self.returned_outcome
            self.terminal_event.set()

    def reqExecutions(self, request_id: int, execution_filter) -> None:
        self.executions_requested = True
        if self.emit_reconciled_execution:
            self.outcome = IbkrOrderOutcome(
                status="FILLED",
                filled_quantity=self.expected_quantity,
                average_fill_price=315.58,
                message="IBKR Paper order filled via execDetails.",
            )
            self.terminal_event.set()
        self.execution_reconciliation_ready.set()

    def cancelOrder(self, order_id: int, manual_cancel_time: str = "") -> None:
        self.cancel_order_called = True


def create_contract() -> Contract:
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract


def create_order() -> IbkrOrder:
    order = IbkrOrder()
    order.action = "BUY"
    order.orderType = "MKT"
    order.totalQuantity = 1
    order.transmit = True
    return order


def create_transport(client: FakeIbkrOrderClient, **kwargs) -> IbkrOrderTransport:
    return IbkrOrderTransport(
        paper_account_id="DU123456",
        allow_order_submission=True,
        connection_timeout_seconds=0.05,
        reconciliation_timeout_seconds=0.05,
        client=client,
        **kwargs,
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
            order=create_order(),
            timeout_seconds=0.05,
        )
    except PermissionError:
        pass
    else:
        raise AssertionError("Expected disabled submission to fail.")
    assert client.connect_called is False


def test_terminal_order_status_returns_fill() -> None:
    client = FakeIbkrOrderClient()
    transport = create_transport(client)
    outcome = transport.submit_order(
        contract=create_contract(),
        order=create_order(),
        timeout_seconds=0.05,
    )
    assert outcome.status == "FILLED"
    assert outcome.filled_quantity == 1
    assert client.executions_requested is False
    assert client.received_order.tif == "DAY"


def test_timeout_reconciles_execution_before_cancel() -> None:
    client = FakeIbkrOrderClient()
    client.emit_terminal_outcome = False
    client.emit_reconciled_execution = True
    transport = create_transport(client)
    outcome = transport.submit_order(
        contract=create_contract(),
        order=create_order(),
        timeout_seconds=0.01,
    )
    assert outcome.status == "FILLED"
    assert outcome.average_fill_price == 315.58
    assert client.executions_requested is True
    assert client.cancel_order_called is False


def test_timeout_cancels_only_after_failed_reconciliation() -> None:
    client = FakeIbkrOrderClient()
    client.emit_terminal_outcome = False
    transport = create_transport(client)
    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_order(),
            timeout_seconds=0.01,
        )
    except TimeoutError as exc:
        assert "execution reconciliation" in str(exc)
    else:
        raise AssertionError("Expected timeout.")
    assert client.executions_requested is True
    assert client.cancel_order_called is True


def test_verifies_configured_account() -> None:
    client = FakeIbkrOrderClient()
    transport = create_transport(client, disconnect_after_order=False)
    transport.submit_order(
        contract=create_contract(),
        order=create_order(),
        timeout_seconds=0.05,
    )
    assert transport.verified_account_id == "DU123456"
    transport.disconnect()


def test_accepts_sell() -> None:
    client = FakeIbkrOrderClient()
    transport = create_transport(client)

    order = create_order()
    order.action = "SELL"

    outcome = transport.submit_order(
        contract=create_contract(),
        order=order,
        timeout_seconds=0.05,
    )

    assert outcome.status == "FILLED"
    assert client.place_order_called is True
    assert client.received_order.action == "SELL"
    assert client.received_order.tif == "DAY"


def test_rejects_missing_account() -> None:
    client = FakeIbkrOrderClient()
    client.returned_managed_accounts = ["DU999999"]

    transport = create_transport(client)

    try:
        transport.submit_order(
            contract=create_contract(),
            order=create_order(),
            timeout_seconds=0.05,
        )
    except IbkrOrderTransportError as exc:
        assert "was not returned" in str(exc)
    else:
        raise AssertionError("Expected account mismatch.")

    assert client.place_order_called is False


def test_rejects_live_port() -> None:
    try:
        IbkrOrderTransport(paper_account_id="DU123456", port=7496)
    except ValueError as exc:
        assert "7497" in str(exc)
    else:
        raise AssertionError("Expected live port rejection.")


def test_rejects_fractional_quantity() -> None:
    client = FakeIbkrOrderClient()
    order = create_order()
    order.totalQuantity = 1.5
    transport = create_transport(client)
    try:
        transport.submit_order(
            contract=create_contract(),
            order=order,
            timeout_seconds=0.05,
        )
    except ValueError as exc:
        assert "whole number" in str(exc)
    else:
        raise AssertionError("Expected fractional quantity rejection.")


def test_disconnect_is_idempotent() -> None:
    client = FakeIbkrOrderClient()
    transport = IbkrOrderTransport(
        paper_account_id="DU123456",
        client=client,
    )
    transport.disconnect()
    transport.disconnect()
    assert transport.is_connected is False


def run() -> None:
    tests = [
        test_submission_is_disabled_by_default,
        test_terminal_order_status_returns_fill,
        test_timeout_reconciles_execution_before_cancel,
        test_timeout_cancels_only_after_failed_reconciliation,
        test_verifies_configured_account,
        test_rejects_missing_account,
        test_rejects_live_port,
        test_accepts_sell,
        test_rejects_fractional_quantity,
        test_disconnect_is_idempotent,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print()
    print(f"IBKR ORDER TRANSPORT TESTS: {len(tests)} passed")


if __name__ == "__main__":
    run()