from __future__ import annotations

import threading

from models.broker_position import BrokerPosition
from services.ibkr.ibkr_account_service import (
    IbkrAccountService,
    IbkrAccountServiceError,
    _IbkrApiError,
    _RawAccountValue,
)


class FakeIbkrAccountClient:
    ACCOUNT_SUMMARY_REQUEST_ID = 9001

    ACCOUNT_TAGS = (
        "NetLiquidation,"
        "TotalCashValue,"
        "AvailableFunds,"
        "BuyingPower,"
        "GrossPositionValue,"
        "UnrealizedPnL,"
        "RealizedPnL,"
        "Currency"
    )

    def __init__(self) -> None:
        self.connection_ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.account_summary_ready = threading.Event()
        self.positions_ready = threading.Event()

        self.next_order_id: int | None = None

        self.returned_managed_accounts: list[str] = [
            "DU123456",
        ]
        self.managed_accounts: list[str] = []

        self.returned_account_summary: dict[
            str,
            dict[str, _RawAccountValue],
        ] = {
            "DU123456": {
                "TotalCashValue": _RawAccountValue(
                    value="10000.50",
                    currency="EUR",
                ),
                "BuyingPower": _RawAccountValue(
                    value="20000.00",
                    currency="EUR",
                ),
                "Currency": _RawAccountValue(
                    value="EUR",
                    currency="",
                ),
            }
        }

        self.account_summary: dict[
            str,
            dict[str, _RawAccountValue],
        ] = {}

        self.returned_positions: list[BrokerPosition] = [
            BrokerPosition(
                account_id="DU123456",
                symbol="AAPL",
                security_type="STK",
                exchange="SMART",
                currency="USD",
                quantity=2.0,
                average_cost=190.0,
            )
        ]

        self.positions: list[BrokerPosition] = []
        self.errors: list[_IbkrApiError] = []

        self.connected = False
        self.connect_called = False
        self.disconnect_called = False
        self.run_called = False

        self.managed_accounts_requested = False
        self.account_summary_requested = False
        self.account_summary_cancelled = False
        self.positions_requested = False
        self.positions_cancelled = False

        self.emit_connection_ready = True
        self.emit_accounts_ready = True
        self.emit_account_summary_ready = True
        self.emit_positions_ready = True

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
            self.next_order_id = 1
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

    def reqAccountSummary(
        self,
        request_id: int,
        group_name: str,
        tags: str,
    ) -> None:
        self.account_summary_requested = True

        if self.emit_account_summary_ready:
            self.account_summary = {
                account_id: dict(values)
                for account_id, values
                in self.returned_account_summary.items()
            }
            self.account_summary_ready.set()

    def cancelAccountSummary(
        self,
        request_id: int,
    ) -> None:
        self.account_summary_cancelled = True

    def reqPositions(self) -> None:
        self.positions_requested = True

        if self.emit_positions_ready:
            self.positions = list(
                self.returned_positions
            )
            self.positions_ready.set()

    def cancelPositions(self) -> None:
        self.positions_cancelled = True


def create_connected_service(
    client: FakeIbkrAccountClient | None = None,
) -> tuple[
    IbkrAccountService,
    FakeIbkrAccountClient,
]:
    fake_client = client or FakeIbkrAccountClient()

    service = IbkrAccountService(
        timeout_seconds=0.1,
        client=fake_client,
    )

    service.connect()

    return service, fake_client


def test_connects_and_selects_single_paper_account() -> None:
    service, client = create_connected_service()

    assert client.connect_called is True
    assert client.run_called is True
    assert client.managed_accounts_requested is True
    assert service.is_connected is True
    assert service.selected_account_id == "DU123456"

    service.disconnect()


def test_maps_account_values_to_broker_account() -> None:
    service, client = create_connected_service()

    account = service.read_account()

    assert account.broker_name == "IBKR"
    assert account.account_id == "DU123456"
    assert account.cash == 10000.50
    assert account.buying_power == 20000.00
    assert account.currency == "EUR"
    assert account.status == "ACTIVE"

    assert client.account_summary_requested is True
    assert client.account_summary_cancelled is True

    service.disconnect()


def test_reads_broker_positions() -> None:
    service, client = create_connected_service()

    positions = service.read_positions()

    assert isinstance(positions, tuple)
    assert len(positions) == 1

    position = positions[0]

    assert position.account_id == "DU123456"
    assert position.symbol == "AAPL"
    assert position.security_type == "STK"
    assert position.exchange == "SMART"
    assert position.currency == "USD"
    assert position.quantity == 2.0
    assert position.average_cost == 190.0

    assert client.positions_requested is True
    assert client.positions_cancelled is True

    service.disconnect()


def test_returns_empty_position_tuple() -> None:
    client = FakeIbkrAccountClient()
    client.returned_positions = []

    service, _ = create_connected_service(client)

    positions = service.read_positions()

    assert positions == ()

    service.disconnect()


def test_rejects_live_account() -> None:
    client = FakeIbkrAccountClient()
    client.returned_managed_accounts = [
        "U123456",
    ]

    service = IbkrAccountService(
        timeout_seconds=0.1,
        client=client,
    )

    try:
        service.connect()
    except IbkrAccountServiceError as exc:
        assert "No DU-prefixed" in str(exc)
    else:
        raise AssertionError(
            "Expected live account selection to fail."
        )

    assert client.disconnect_called is True


def test_rejects_multiple_paper_accounts_without_configuration() -> None:
    client = FakeIbkrAccountClient()
    client.returned_managed_accounts = [
        "DU123456",
        "DU654321",
    ]

    service = IbkrAccountService(
        timeout_seconds=0.1,
        client=client,
    )

    try:
        service.connect()
    except IbkrAccountServiceError as exc:
        assert "Multiple IBKR Paper accounts" in str(exc)
    else:
        raise AssertionError(
            "Expected multiple paper accounts to fail."
        )

    assert client.disconnect_called is True


def test_selects_expected_paper_account() -> None:
    client = FakeIbkrAccountClient()
    client.returned_managed_accounts = [
        "DU123456",
        "DU654321",
    ]

    service = IbkrAccountService(
        timeout_seconds=0.1,
        expected_account_id="du654321",
        client=client,
    )

    service.connect()

    assert service.selected_account_id == "DU654321"

    service.disconnect()


def test_rejects_missing_expected_paper_account() -> None:
    client = FakeIbkrAccountClient()
    client.returned_managed_accounts = [
        "DU123456",
    ]

    service = IbkrAccountService(
        timeout_seconds=0.1,
        expected_account_id="DU999999",
        client=client,
    )

    try:
        service.connect()
    except IbkrAccountServiceError as exc:
        assert "was not returned by TWS" in str(exc)
    else:
        raise AssertionError(
            "Expected missing configured account to fail."
        )

    assert client.disconnect_called is True


def test_connection_timeout_disconnects_client() -> None:
    client = FakeIbkrAccountClient()
    client.emit_connection_ready = False

    service = IbkrAccountService(
        timeout_seconds=0.01,
        client=client,
    )

    try:
        service.connect()
    except IbkrAccountServiceError as exc:
        assert "TWS connection readiness" in str(exc)
    else:
        raise AssertionError(
            "Expected connection readiness timeout."
        )

    assert client.disconnect_called is True
    assert service.is_connected is False


def test_account_summary_timeout_cancels_request() -> None:
    client = FakeIbkrAccountClient()
    client.emit_account_summary_ready = False

    service, _ = create_connected_service(client)

    try:
        service.read_account()
    except IbkrAccountServiceError as exc:
        assert "account summary" in str(exc)
    else:
        raise AssertionError(
            "Expected account summary timeout."
        )

    assert client.account_summary_cancelled is True

    service.disconnect()


def test_positions_timeout_cancels_request() -> None:
    client = FakeIbkrAccountClient()
    client.emit_positions_ready = False

    service, _ = create_connected_service(client)

    try:
        service.read_positions()
    except IbkrAccountServiceError as exc:
        assert "position list" in str(exc)
    else:
        raise AssertionError(
            "Expected position list timeout."
        )

    assert client.positions_cancelled is True

    service.disconnect()


def test_rejects_missing_cash_value() -> None:
    client = FakeIbkrAccountClient()

    del client.returned_account_summary[
        "DU123456"
    ]["TotalCashValue"]

    service, _ = create_connected_service(client)

    try:
        service.read_account()
    except IbkrAccountServiceError as exc:
        assert "TotalCashValue was not returned" in str(exc)
    else:
        raise AssertionError(
            "Expected missing cash value to fail."
        )

    assert client.account_summary_cancelled is True

    service.disconnect()


def test_rejects_non_finite_buying_power() -> None:
    client = FakeIbkrAccountClient()

    client.returned_account_summary[
        "DU123456"
    ]["BuyingPower"] = _RawAccountValue(
        value="nan",
        currency="EUR",
    )

    service, _ = create_connected_service(client)

    try:
        service.read_account()
    except IbkrAccountServiceError as exc:
        assert (
            "BuyingPower contained a non-finite value"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected non-finite buying power to fail."
        )

    assert client.account_summary_cancelled is True

    service.disconnect()


def test_rejects_conflicting_account_currencies() -> None:
    client = FakeIbkrAccountClient()

    client.returned_account_summary[
        "DU123456"
    ]["BuyingPower"] = _RawAccountValue(
        value="20000.00",
        currency="USD",
    )

    service, _ = create_connected_service(client)

    try:
        service.read_account()
    except IbkrAccountServiceError as exc:
        assert "Conflicting account currencies" in str(exc)
    else:
        raise AssertionError(
            "Expected conflicting currencies to fail."
        )

    service.disconnect()


def test_rejects_position_for_unexpected_account() -> None:
    client = FakeIbkrAccountClient()

    client.returned_positions = [
        BrokerPosition(
            account_id="DU999999",
            symbol="MSFT",
            security_type="STK",
            exchange="SMART",
            currency="USD",
            quantity=1.0,
            average_cost=400.0,
        )
    ]

    service, _ = create_connected_service(client)

    try:
        service.read_positions()
    except IbkrAccountServiceError as exc:
        assert "unexpected account" in str(exc)
    else:
        raise AssertionError(
            "Expected unexpected position account to fail."
        )

    assert client.positions_cancelled is True

    service.disconnect()


def test_serious_api_error_fails_operation() -> None:
    service, client = create_connected_service()

    client.errors = [
        _IbkrApiError(
            request_id=9001,
            error_code=502,
            message="Could not connect to TWS.",
        )
    ]

    try:
        service._raise_if_errors("test operation")
    except IbkrAccountServiceError as exc:
        assert "code=502" in str(exc)
        assert "test operation" in str(exc)
    else:
        raise AssertionError(
            "Expected serious API error to fail."
        )

    service.disconnect()


def test_disconnect_is_idempotent() -> None:
    service, client = create_connected_service()

    service.disconnect()
    service.disconnect()

    assert service.is_connected is False
    assert service.selected_account_id is None
    assert client.disconnect_called is True


def test_requires_connection_before_account_read() -> None:
    client = FakeIbkrAccountClient()

    service = IbkrAccountService(
        timeout_seconds=0.1,
        client=client,
    )

    try:
        service.read_account()
    except IbkrAccountServiceError as exc:
        assert "not connected" in str(exc)
    else:
        raise AssertionError(
            "Expected disconnected account read to fail."
        )


def run() -> None:
    tests = [
        test_connects_and_selects_single_paper_account,
        test_maps_account_values_to_broker_account,
        test_reads_broker_positions,
        test_returns_empty_position_tuple,
        test_rejects_live_account,
        test_rejects_multiple_paper_accounts_without_configuration,
        test_selects_expected_paper_account,
        test_rejects_missing_expected_paper_account,
        test_connection_timeout_disconnects_client,
        test_account_summary_timeout_cancels_request,
        test_positions_timeout_cancels_request,
        test_rejects_missing_cash_value,
        test_rejects_non_finite_buying_power,
        test_rejects_conflicting_account_currencies,
        test_rejects_position_for_unexpected_account,
        test_serious_api_error_fails_operation,
        test_disconnect_is_idempotent,
        test_requires_connection_before_account_read,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR ACCOUNT SERVICE TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()