from __future__ import annotations

import math
import threading
import time
from dataclasses import dataclass

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


@dataclass(frozen=True)
class IbkrPositionSnapshot:
    account: str
    symbol: str
    security_type: str
    exchange: str
    currency: str
    quantity: float
    average_cost: float


class IbkrAccountReader(EWrapper, EClient):
    """
    Read-only IBKR TWS Paper account reader.

    Reads:
    - managed account identifiers;
    - account summary values;
    - current broker positions.

    This client does not submit, modify or cancel orders.
    """

    ACCOUNT_SUMMARY_REQUEST_ID = 9001

    ACCOUNT_TAGS = ",".join(
        (
            "NetLiquidation",
            "TotalCashValue",
            "AvailableFunds",
            "BuyingPower",
            "GrossPositionValue",
            "UnrealizedPnL",
            "RealizedPnL",
            "Currency",
        )
    )

    INFORMATIONAL_ERROR_CODES = {
        2104,
        2106,
        2107,
        2108,
        2158,
    }

    def __init__(self) -> None:
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.connection_ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.account_summary_ready = threading.Event()
        self.positions_ready = threading.Event()

        self.next_order_id: int | None = None
        self.managed_accounts: list[str] = []

        self.account_summary: dict[
            str,
            dict[str, dict[str, str]],
        ] = {}

        self.positions: list[
            IbkrPositionSnapshot
        ] = []

        self.errors: list[str] = []

    def nextValidId(
        self,
        orderId: int,
    ) -> None:
        self.next_order_id = int(orderId)
        self.connection_ready.set()

    def managedAccounts(
        self,
        accountsList: str,
    ) -> None:
        self.managed_accounts = [
            account.strip()
            for account in accountsList.split(",")
            if account.strip()
        ]

        self.accounts_ready.set()

    def accountSummary(
        self,
        reqId: int,
        account: str,
        tag: str,
        value: str,
        currency: str,
    ) -> None:
        account_values = (
            self.account_summary
            .setdefault(account, {})
        )

        account_values[tag] = {
            "value": value,
            "currency": currency,
        }

    def accountSummaryEnd(
        self,
        reqId: int,
    ) -> None:
        if (
            reqId
            == self.ACCOUNT_SUMMARY_REQUEST_ID
        ):
            self.account_summary_ready.set()

    def position(
        self,
        account: str,
        contract: Contract,
        position,
        avgCost: float,
    ) -> None:
        quantity = float(position)
        average_cost = float(avgCost)

        if not math.isfinite(quantity):
            self.errors.append(
                "Non-finite position quantity "
                f"received for {contract.symbol!r}."
            )
            return

        if not math.isfinite(average_cost):
            self.errors.append(
                "Non-finite average cost "
                f"received for {contract.symbol!r}."
            )
            return

        self.positions.append(
            IbkrPositionSnapshot(
                account=str(account).strip(),
                symbol=str(
                    contract.symbol
                ).strip().upper(),
                security_type=str(
                    contract.secType
                ).strip().upper(),
                exchange=str(
                    contract.exchange
                ).strip().upper(),
                currency=str(
                    contract.currency
                ).strip().upper(),
                quantity=quantity,
                average_cost=average_cost,
            )
        )

    def positionEnd(self) -> None:
        self.positions_ready.set()

    def error(
        self,
        reqId,
        errorCode,
        errorString,
        advancedOrderRejectJson="",
    ) -> None:
        message = (
            f"reqId={reqId}, "
            f"code={errorCode}, "
            f"message={errorString}"
        )

        if errorCode in (
            self.INFORMATIONAL_ERROR_CODES
        ):
            print(f"IBKR INFO: {message}")
            return

        self.errors.append(message)
        print(f"IBKR ERROR: {message}")


def run_network_loop(
    client: IbkrAccountReader,
) -> None:
    client.run()


def require_event(
    event: threading.Event,
    *,
    timeout_seconds: float,
    description: str,
) -> None:
    if not event.wait(timeout_seconds):
        raise TimeoutError(
            f"Timeout while waiting for "
            f"{description}."
        )


def format_account_value(
    item: dict[str, str] | None,
) -> str:
    if item is None:
        return "not returned"

    value = item.get("value", "")
    currency = item.get("currency", "")

    if currency:
        return f"{value} {currency}"

    return value or "not returned"


def print_account_summary(
    client: IbkrAccountReader,
    account: str,
) -> None:
    values = client.account_summary.get(
        account,
        {},
    )

    print()
    print("ACCOUNT SUMMARY")
    print("-----------------------------------------")
    print(f"Account:              {account}")
    print(
        "Net liquidation:      "
        + format_account_value(
            values.get("NetLiquidation")
        )
    )
    print(
        "Total cash value:     "
        + format_account_value(
            values.get("TotalCashValue")
        )
    )
    print(
        "Available funds:      "
        + format_account_value(
            values.get("AvailableFunds")
        )
    )
    print(
        "Buying power:         "
        + format_account_value(
            values.get("BuyingPower")
        )
    )
    print(
        "Gross position value: "
        + format_account_value(
            values.get("GrossPositionValue")
        )
    )
    print(
        "Unrealized P&L:       "
        + format_account_value(
            values.get("UnrealizedPnL")
        )
    )
    print(
        "Realized P&L:         "
        + format_account_value(
            values.get("RealizedPnL")
        )
    )


def print_positions(
    positions: list[IbkrPositionSnapshot],
) -> None:
    print()
    print("POSITIONS")
    print("-----------------------------------------")

    if not positions:
        print("No open IBKR positions.")
        return

    for position in positions:
        print(
            f"{position.symbol}: "
            f"quantity={position.quantity}, "
            f"average_cost={position.average_cost:.4f}, "
            f"currency={position.currency}, "
            f"type={position.security_type}"
        )


def main() -> None:
    host = "127.0.0.1"
    port = 7497
    client_id = 102
    timeout_seconds = 15.0

    client = IbkrAccountReader()

    print()
    print("=========================================")
    print("IBKR PAPER ACCOUNT READER")
    print("=========================================")
    print(f"Host:      {host}")
    print(f"Port:      {port}")
    print(f"Client ID: {client_id}")
    print("Mode:      READ ONLY")
    print("Orders:    NOT SUPPORTED BY THIS SCRIPT")
    print("=========================================")

    network_thread: threading.Thread | None = None

    try:
        client.connect(
            host,
            port,
            clientId=client_id,
        )

        network_thread = threading.Thread(
            target=run_network_loop,
            args=(client,),
            daemon=True,
        )
        network_thread.start()

        require_event(
            client.connection_ready,
            timeout_seconds=timeout_seconds,
            description="TWS connection readiness",
        )

        client.reqManagedAccts()

        require_event(
            client.accounts_ready,
            timeout_seconds=timeout_seconds,
            description="managed accounts",
        )

        paper_accounts = [
            account
            for account in client.managed_accounts
            if account.upper().startswith("DU")
        ]

        if not paper_accounts:
            raise RuntimeError(
                "No DU-prefixed paper account "
                "was returned by TWS."
            )

        client.reqAccountSummary(
            client.ACCOUNT_SUMMARY_REQUEST_ID,
            "All",
            client.ACCOUNT_TAGS,
        )

        client.reqPositions()

        require_event(
            client.account_summary_ready,
            timeout_seconds=timeout_seconds,
            description="account summary",
        )

        require_event(
            client.positions_ready,
            timeout_seconds=timeout_seconds,
            description="position list",
        )

        client.cancelAccountSummary(
            client.ACCOUNT_SUMMARY_REQUEST_ID
        )
        client.cancelPositions()

        for account in paper_accounts:
            print_account_summary(
                client,
                account,
            )

        print_positions(client.positions)

        serious_errors = [
            error
            for error in client.errors
            if "code=502" not in error
        ]

        if serious_errors:
            print()
            print("NON-INFORMATIONAL API MESSAGES")
            print("-----------------------------------------")

            for error in serious_errors:
                print(error)

        print()
        print("Connection:          PASS")
        print(
            "Paper accounts:      "
            f"{', '.join(paper_accounts)}"
        )
        print(
            "Positions returned:  "
            f"{len(client.positions)}"
        )
        print()
        print("IBKR ACCOUNT READER: PASS")

    finally:
        if client.isConnected():
            client.disconnect()

        if network_thread is not None:
            network_thread.join(
                timeout=2.0
            )

        time.sleep(0.25)


if __name__ == "__main__":
    main()