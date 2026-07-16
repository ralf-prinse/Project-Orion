from __future__ import annotations

from ibapi.contract import Contract
from ibapi.order import Order

from services.ibkr.ibkr_order_transport import (
    IbkrOrderTransport,
)


def create_contract() -> Contract:
    contract = Contract()

    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    return contract


def create_sell_order() -> Order:
    order = Order()

    order.action = "SELL"
    order.orderType = "MKT"
    order.totalQuantity = 1
    order.transmit = True

    return order


def test_sell_validation():
    transport = IbkrOrderTransport(
        paper_account_id="DU123456",
    )

    quantity = transport._validate_ibkr_order(
        create_sell_order()
    )

    assert quantity == 1


def run():
    test_sell_validation()

    print()
    print("IBKR SELL VALIDATION: PASS")


if __name__ == "__main__":
    run()