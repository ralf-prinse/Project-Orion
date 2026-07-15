from __future__ import annotations

import threading

from ibapi.contract import Contract
from ibapi.order import Order as IbkrOrder

from services.ibkr.ibkr_broker import IbkrOrderOutcome
from services.ibkr.ibkr_order_transport import IbkrOrderTransport


class FakeLateFillClient:
    EXECUTION_RECONCILIATION_REQUEST_ID = 9101

    def __init__(self) -> None:
        self.connection_ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.terminal_event = threading.Event()
        self.execution_reconciliation_ready = threading.Event()

        self.connected = False
        self.next_order_id = 1
        self.active_order_id = None
        self.expected_quantity = 0

        self.managed_accounts = ["DU123456"]
        self.errors = []
        self.outcome = None

        self.reconciliation_calls = 0
        self.cancel_called = False

    def reset_connection_state(self):
        self.connection_ready.clear()
        self.accounts_ready.clear()
        self.execution_reconciliation_ready.clear()

    def connect(self, host, port, clientId):
        self.connected = True

    def run(self):
        self.connection_ready.set()

    def isConnected(self):
        return self.connected

    def disconnect(self):
        self.connected = False

    def reqManagedAccts(self):
        self.managed_accounts = ["DU123456"]
        self.accounts_ready.set()

    def reset_order_state(self, order_id, expected_quantity):
        self.active_order_id = order_id
        self.expected_quantity = expected_quantity
        self.outcome = None
        self.terminal_event.clear()
        self.execution_reconciliation_ready.clear()

    def placeOrder(self, order_id, contract, order):
        pass

    def reqExecutions(self, request_id, execution_filter):
        self.reconciliation_calls += 1

        if self.reconciliation_calls == 2:
            self.outcome = IbkrOrderOutcome(
                status="FILLED",
                filled_quantity=self.expected_quantity,
                average_fill_price=15.7711,
                message="Late execution reconciliation",
            )
            self.terminal_event.set()

        self.execution_reconciliation_ready.set()

    def cancelOrder(self, order_id, manual_cancel_time=""):
        self.cancel_called = True


def create_contract():
    c = Contract()
    c.symbol = "AAL"
    c.secType = "STK"
    c.exchange = "SMART"
    c.currency = "USD"
    return c


def create_order():
    o = IbkrOrder()
    o.action = "BUY"
    o.orderType = "MKT"
    o.totalQuantity = 9
    o.transmit = True
    return o


def test_late_fill_reconciliation():
    client = FakeLateFillClient()

    transport = IbkrOrderTransport(
        paper_account_id="DU123456",
        allow_order_submission=True,
        connection_timeout_seconds=0.05,
        reconciliation_timeout_seconds=0.05,
        client=client,
    )

    try:
        outcome = transport.submit_order(
            contract=create_contract(),
            order=create_order(),
            timeout_seconds=0.01,
        )
    finally:
        transport.disconnect()

    assert outcome.status == "FILLED"
    assert outcome.filled_quantity == 9
    assert client.reconciliation_calls == 2
    assert client.cancel_called is False


def run():
    test_late_fill_reconciliation()

    print()
    print("LATE FILL RECONCILIATION: PASS")


if __name__ == "__main__":
    run()