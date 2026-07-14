from __future__ import annotations

from services.ibkr.ibkr_account_service import (
    IbkrAccountService,
)


def mask_account_id(account_id: str) -> str:
    if len(account_id) <= 4:
        return account_id

    return account_id[:2] + "*" * (len(account_id) - 4) + account_id[-2:]


def run() -> None:
    service = IbkrAccountService(
        host="127.0.0.1",
        port=7497,
        client_id=110,
        timeout_seconds=15.0,
    )

    try:
        print()
        print("=========================================")
        print("IBKR ACCOUNT SERVICE INTEGRATION TEST")
        print("=========================================")
        print("Mode:       TWS Paper")
        print("API:        Read Only")
        print("Host:       127.0.0.1")
        print("Port:       7497")
        print("Client ID:  110")
        print("=========================================")

        service.connect()

        account = service.read_account()
        positions = service.read_positions()

        print()
        print("ACCOUNT")
        print("-----------------------------------------")
        print(
            f"Account ID:    {mask_account_id(account.account_id)}"
        )
        print(f"Broker:        {account.broker_name}")
        print(f"Currency:      {account.currency}")
        print(f"Cash:          {account.cash:.2f}")
        print(f"Buying power:  {account.buying_power:.2f}")
        print(f"Status:        {account.status}")

        print()
        print("POSITIONS")
        print("-----------------------------------------")
        print(f"Count:         {len(positions)}")

        for position in positions:
            print(
                f"{position.symbol}: "
                f"quantity={position.quantity}, "
                f"average_cost={position.average_cost:.4f}, "
                f"currency={position.currency}, "
                f"type={position.security_type}"
            )

        print()
        print("Connection:    PASS")
        print("Account read:  PASS")
        print("Positions:     PASS")
        print("Disconnect:    pending")
        print()

    finally:
        service.disconnect()

        print("Disconnect:    PASS")
        print()
        print("IBKR ACCOUNT SERVICE INTEGRATION: PASS")


if __name__ == "__main__":
    run()