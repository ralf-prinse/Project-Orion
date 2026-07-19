from __future__ import annotations

from ibapi.contract import Contract
from ibapi.order import Order

from services.ibkr.ibkr_order_transport import (
    IbkrOrderTransport,
)
from services.ibkr.ibkr_broker import IbkrBroker


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


def test_german_stock_contract_uses_xetra_primary_exchange():
    broker = IbkrBroker(transport=object())
    contract = broker._build_contract(
        type("Order", (), {"symbol": "SAP.DE"})()
    )

    assert contract.symbol == "SAP"
    assert contract.exchange == "SMART"
    assert contract.currency == "EUR"
    assert contract.primaryExchange == "IBIS"


def run():
    test_sell_validation()

    print()
    print("IBKR SELL VALIDATION: PASS")


if __name__ == "__main__":
    run()
