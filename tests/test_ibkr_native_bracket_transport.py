from ibapi.order import Order as IbkrOrder
import threading
from datetime import datetime

from test_ibkr_order_transport import (
    FakeIbkrOrderClient,
    create_contract,
    create_order,
    create_transport,
)
from services.ibkr.ibkr_order_transport import IbkrProtectiveExecution


def test_transport_claims_three_ids_and_returns_child_ids():
    client = FakeIbkrOrderClient()
    transport = create_transport(client)
    parent = create_order()
    parent.transmit = False

    take_profit = IbkrOrder()
    take_profit.action = "SELL"
    take_profit.orderType = "LMT"
    take_profit.totalQuantity = 1
    take_profit.lmtPrice = 108.0
    take_profit.transmit = False

    stop_loss = IbkrOrder()
    stop_loss.action = "SELL"
    stop_loss.orderType = "STP"
    stop_loss.totalQuantity = 1
    stop_loss.auxPrice = 96.0
    stop_loss.transmit = True

    outcome = transport.submit_bracket_order(
        contract=create_contract(),
        parent_order=parent,
        take_profit_order=take_profit,
        stop_loss_order=stop_loss,
        timeout_seconds=0.05,
    )

    assert outcome.order_id == 500
    assert outcome.child_order_ids == (501, 502)
    assert parent.orderId == 500
    assert take_profit.parentId == 500
    assert stop_loss.parentId == 500
    assert stop_loss.orderId == 502


class FakeHistoryClient(FakeIbkrOrderClient):
    EXECUTION_HISTORY_REQUEST_ID = 9102

    def __init__(self):
        super().__init__()
        self.execution_history_ready = threading.Event()
        self.execution_history = []

    def begin_execution_history(self):
        self.execution_history_ready.clear()
        self.execution_history = []

    def reqExecutions(self, request_id, execution_filter):
        if request_id == self.EXECUTION_HISTORY_REQUEST_ID:
            self.execution_history = [
                IbkrProtectiveExecution(
                    symbol="AAPL",
                    order_reference="trade-1:SL",
                    side="SLD",
                    quantity=2,
                    price=96.0,
                    executed_at=datetime(2026, 7, 19, 15, 0),
                    order_id=502,
                )
            ]
            self.execution_history_ready.set()
            return
        super().reqExecutions(request_id, execution_filter)


def test_transport_finds_protective_execution_by_trade_reference():
    transport = create_transport(FakeHistoryClient())
    execution = transport.find_protective_exit(
        trade_id="trade-1",
        symbol="AAPL",
        timeout_seconds=0.05,
    )
    assert execution is not None
    assert execution.order_reference == "trade-1:SL"
    assert execution.price == 96.0
