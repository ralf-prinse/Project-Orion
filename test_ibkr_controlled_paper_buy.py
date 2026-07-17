from __future__ import annotations

import os
from datetime import datetime

from models.order import Order
from services.ibkr.ibkr_broker import IbkrBroker
from services.ibkr.ibkr_order_transport import (
    IbkrOrderTransport,
)


EXPECTED_CONFIRMATION = "PLACE ONE IBKR PAPER BUY"
SYMBOL="ASML.AS"
QUANTITY = 1
REFERENCE_PRICE = 250.0
PAPER_PORT = 7497
CLIENT_ID = 130


def mask_account_id(account_id: str) -> str:
    if len(account_id) <= 4:
        return account_id

    return (
        account_id[:2]
        + "*" * (len(account_id) - 4)
        + account_id[-2:]
    )


def require_paper_account_id() -> str:
    account_id = os.environ.get(
        "ORION_IBKR_PAPER_ACCOUNT_ID",
        "",
    ).strip().upper()

    if not account_id:
        raise RuntimeError(
            "Environment variable "
            "ORION_IBKR_PAPER_ACCOUNT_ID is not set."
        )

    if not account_id.startswith("DU"):
        raise RuntimeError(
            "ORION_IBKR_PAPER_ACCOUNT_ID must start with 'DU'."
        )

    return account_id


def show_preflight(account_id: str) -> None:
    print()
    print("=========================================")
    print("ORION CONTROLLED IBKR PAPER BUY")
    print("=========================================")
    print(f"Account:        {mask_account_id(account_id)}")
    print("Host:           127.0.0.1")
    print(f"Port:           {PAPER_PORT}")
    print(f"Client ID:      {CLIENT_ID}")
    print("Mode:           PAPER ONLY")
    print(f"Symbol:         {SYMBOL}")
    print("Side:           BUY")
    print("Order type:     MARKET")
    print(f"Quantity:       {QUANTITY}")
    print("Automatic retry: NO")
    print("Continuous loop: NO")
    print("=========================================")
    print()
    print(
        "This will submit exactly one simulated BUY order "
        "to the connected IBKR Paper account."
    )
    print()


def require_confirmation() -> None:
    confirmation = input(
        f"Type exactly '{EXPECTED_CONFIRMATION}' to continue: "
    ).strip()

    if confirmation != EXPECTED_CONFIRMATION:
        raise RuntimeError(
            "Confirmation did not match. "
            "No order was submitted."
        )


def build_orion_order() -> Order:
    return Order(
        symbol=SYMBOL,
        side="BUY",
        quantity=QUANTITY,
        order_type="MARKET",
        price=REFERENCE_PRICE,
        created_at=datetime.now(),
        source="ControlledIbkrPaperBuy",
    )


def run() -> None:
    account_id = require_paper_account_id()

    show_preflight(account_id)
    require_confirmation()

    transport = IbkrOrderTransport(
        paper_account_id=account_id,
        host="127.0.0.1",
        port=PAPER_PORT,
        client_id=CLIENT_ID,
        connection_timeout_seconds=15.0,
        allow_order_submission=True,
        disconnect_after_order=True,
    )

    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=30.0,
        exchange="SMART",
        currency="USD",
    )

    order = build_orion_order()

    print()
    print("Submitting one controlled IBKR Paper BUY...")
    print()

    result = broker.execute(order)

    print("=========================================")
    print("EXECUTION RESULT")
    print("=========================================")
    print(f"Accepted:          {result.accepted}")
    print(f"Status:            {result.status}")
    print(f"Message:           {result.message}")
    print(f"Executed quantity: {result.executed_quantity}")
    print(f"Executed price:    {result.executed_price:.4f}")
    print(f"Executed at:       {result.executed_at}")
    print("=========================================")

    if not result.accepted:
        raise RuntimeError(
            "Controlled IBKR Paper BUY was not accepted. "
            "Review the execution result before doing anything else."
        )

    if result.status != "FILLED":
        raise RuntimeError(
            "Controlled order did not finish as FILLED."
        )

    if result.executed_quantity != QUANTITY:
        raise RuntimeError(
            "Executed quantity did not match the requested quantity."
        )

    print()
    print("CONTROLLED IBKR PAPER BUY: PASS")
    print("Do not run this script a second time.")
    print()


if __name__ == "__main__":
    run()