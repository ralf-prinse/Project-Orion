from __future__ import annotations

import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class IbkrConnectionTest(EWrapper, EClient):
    """
    Minimal read-only connectivity test for TWS Paper Trading.

    Connects to TWS, waits for a valid order ID and managed accounts,
    then disconnects cleanly.

    No orders are submitted.
    """

    def __init__(self) -> None:
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.connected_event = threading.Event()
        self.accounts_event = threading.Event()

        self.next_order_id: int | None = None
        self.managed_accounts: list[str] = []
        self.errors: list[str] = []

    def nextValidId(
        self,
        orderId: int,
    ) -> None:
        self.next_order_id = orderId
        self.connected_event.set()

    def managedAccounts(
        self,
        accountsList: str,
    ) -> None:
        self.managed_accounts = [
            account.strip()
            for account in accountsList.split(",")
            if account.strip()
        ]
        self.accounts_event.set()

    def error(
        self,
        reqId,
        errorCode,
        errorString,
        advancedOrderRejectJson="",
    ) -> None:
        informational_codes = {
            2104,
            2106,
            2107,
            2108,
            2158,
        }

        message = (
            f"reqId={reqId}, "
            f"code={errorCode}, "
            f"message={errorString}"
        )

        if errorCode in informational_codes:
            print(f"IBKR INFO: {message}")
            return

        self.errors.append(message)
        print(f"IBKR ERROR: {message}")


def run_network_loop(
    client: IbkrConnectionTest,
) -> None:
    client.run()


def main() -> None:
    host = "127.0.0.1"
    port = 7497
    client_id = 101

    client = IbkrConnectionTest()

    print()
    print("=========================================")
    print("IBKR TWS PAPER CONNECTION TEST")
    print("=========================================")
    print(f"Host:      {host}")
    print(f"Port:      {port}")
    print(f"Client ID: {client_id}")
    print("Orders:    disabled by TWS read-only mode")
    print("=========================================")
    print()

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

        if not client.connected_event.wait(
            timeout=10
        ):
            raise TimeoutError(
                "No nextValidId received from TWS "
                "within 10 seconds."
            )

        client.reqManagedAccts()

        if not client.accounts_event.wait(
            timeout=10
        ):
            raise TimeoutError(
                "No managed account list received "
                "within 10 seconds."
            )

        if not client.isConnected():
            raise ConnectionError(
                "IBKR client disconnected unexpectedly."
            )

        if not client.managed_accounts:
            raise RuntimeError(
                "No IBKR accounts were returned."
            )

        paper_accounts = [
            account
            for account in client.managed_accounts
            if account.upper().startswith("DU")
        ]

        if not paper_accounts:
            raise RuntimeError(
                "No DU-prefixed paper account was found."
            )

        print("Connection:       PASS")
        print(
            "Next order ID:    "
            f"{client.next_order_id}"
        )
        print(
            "Managed accounts: "
            f"{', '.join(client.managed_accounts)}"
        )
        print(
            "Paper account:    "
            f"{paper_accounts[0]}"
        )
        print()
        print("IBKR CONNECTION TEST: PASS")

    finally:
        if client.isConnected():
            client.disconnect()

        time.sleep(0.5)


if __name__ == "__main__":
    main()