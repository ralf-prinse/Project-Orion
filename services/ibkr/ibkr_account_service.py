from __future__ import annotations

import math
import threading
from dataclasses import dataclass

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition


class IbkrAccountServiceError(RuntimeError):
    """
    Raised when the IBKR account service cannot complete a reliable
    read-only account operation.
    """


@dataclass(frozen=True)
class _IbkrApiError:
    request_id: int
    error_code: int
    message: str
    advanced_reject_json: str = ""


@dataclass(frozen=True)
class _RawAccountValue:
    value: str
    currency: str


class _IbkrAccountClient(EWrapper, EClient):
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
            dict[str, _RawAccountValue],
        ] = {}

        self.positions: list[BrokerPosition] = []
        self.errors: list[_IbkrApiError] = []

    def nextValidId(self, orderId: int) -> None:
        self.next_order_id = int(orderId)
        self.connection_ready.set()

    def managedAccounts(self, accountsList: str) -> None:
        accounts = [
            account.strip()
            for account in accountsList.split(",")
            if account.strip()
        ]

        self.managed_accounts = list(dict.fromkeys(accounts))
        self.accounts_ready.set()

    def accountSummary(
        self,
        reqId: int,
        account: str,
        tag: str,
        value: str,
        currency: str,
    ) -> None:
        if reqId != self.ACCOUNT_SUMMARY_REQUEST_ID:
            return

        account_id = str(account).strip()
        account_values = self.account_summary.setdefault(
            account_id,
            {},
        )

        account_values[str(tag).strip()] = _RawAccountValue(
            value=str(value).strip(),
            currency=str(currency).strip().upper(),
        )

    def accountSummaryEnd(self, reqId: int) -> None:
        if reqId == self.ACCOUNT_SUMMARY_REQUEST_ID:
            self.account_summary_ready.set()

    def position(
        self,
        account: str,
        contract: Contract,
        position,
        avgCost: float,
    ) -> None:
        try:
            quantity = float(position)
            average_cost = float(avgCost)
        except (TypeError, ValueError) as exc:
            self.errors.append(
                _IbkrApiError(
                    request_id=-1,
                    error_code=-1,
                    message=(
                        "Invalid numeric position value received "
                        f"for {getattr(contract, 'symbol', '')!r}: {exc}"
                    ),
                )
            )
            return

        if not math.isfinite(quantity):
            self.errors.append(
                _IbkrApiError(
                    request_id=-1,
                    error_code=-1,
                    message=(
                        "Non-finite position quantity received "
                        f"for {getattr(contract, 'symbol', '')!r}."
                    ),
                )
            )
            return

        if not math.isfinite(average_cost):
            self.errors.append(
                _IbkrApiError(
                    request_id=-1,
                    error_code=-1,
                    message=(
                        "Non-finite average cost received "
                        f"for {getattr(contract, 'symbol', '')!r}."
                    ),
                )
            )
            return

        if quantity == 0:
            return

        self.positions.append(
            BrokerPosition(
                account_id=str(account).strip(),
                symbol=str(contract.symbol).strip().upper(),
                security_type=str(contract.secType).strip().upper(),
                exchange=str(contract.exchange).strip().upper(),
                currency=str(contract.currency).strip().upper(),
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
        error_code = int(errorCode)

        if error_code in self.INFORMATIONAL_ERROR_CODES:
            return

        self.errors.append(
            _IbkrApiError(
                request_id=int(reqId),
                error_code=error_code,
                message=str(errorString),
                advanced_reject_json=str(
                    advancedOrderRejectJson or ""
                ),
            )
        )


class IbkrAccountService:
    """
    Production read-only service for IBKR TWS Paper accounts.

    Responsibilities:
    - connect to TWS Paper;
    - identify the configured paper account;
    - read account values;
    - read broker positions;
    - map broker data to Orion models;
    - disconnect cleanly.

    This service never submits, modifies or cancels orders.
    """

    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 7497,
        client_id: int = 110,
        timeout_seconds: float = 15.0,
        expected_account_id: str | None = None,
        client: _IbkrAccountClient | None = None,
    ) -> None:
        if not host.strip():
            raise ValueError("IBKR host must not be empty.")

        if port <= 0:
            raise ValueError("IBKR port must be greater than zero.")

        if timeout_seconds <= 0:
            raise ValueError(
                "IBKR timeout_seconds must be greater than zero."
            )

        normalized_account_id = (
            expected_account_id.strip().upper()
            if expected_account_id
            else None
        )

        if (
            normalized_account_id is not None
            and not normalized_account_id.startswith("DU")
        ):
            raise ValueError(
                "expected_account_id must reference an IBKR "
                "Paper account starting with 'DU'."
            )

        self.host = host.strip()
        self.port = int(port)
        self.client_id = int(client_id)
        self.timeout_seconds = float(timeout_seconds)
        self.expected_account_id = normalized_account_id

        self._client = client or _IbkrAccountClient()
        self._network_thread: threading.Thread | None = None
        self._selected_account_id: str | None = None

    @property
    def is_connected(self) -> bool:
        return bool(self._client.isConnected())

    @property
    def selected_account_id(self) -> str | None:
        return self._selected_account_id

    def connect(self) -> None:
        if self.is_connected:
            return

        self._reset_connection_state()

        try:
            self._client.connect(
                self.host,
                self.port,
                clientId=self.client_id,
            )

            self._network_thread = threading.Thread(
                target=self._client.run,
                name="ibkr-account-service",
                daemon=True,
            )
            self._network_thread.start()

            self._wait_for_event(
                self._client.connection_ready,
                description="TWS connection readiness",
            )

            self._raise_if_errors("connecting to TWS")

            self._client.reqManagedAccts()

            self._wait_for_event(
                self._client.accounts_ready,
                description="managed accounts",
            )

            self._raise_if_errors("reading managed accounts")
            self._selected_account_id = self._select_paper_account()

        except Exception:
            self.disconnect()
            raise

    def read_account(self) -> BrokerAccount:
        self._require_connected()

        account_id = self._require_selected_account()

        self._client.account_summary_ready.clear()
        self._client.account_summary = {}
        self._clear_errors()

        request_started = False

        try:
            self._client.reqAccountSummary(
                self._client.ACCOUNT_SUMMARY_REQUEST_ID,
                "All",
                self._client.ACCOUNT_TAGS,
            )
            request_started = True

            self._wait_for_event(
                self._client.account_summary_ready,
                description="account summary",
            )

            self._raise_if_errors("reading account summary")

            account_values = self._client.account_summary.get(
                account_id
            )

            if account_values is None:
                raise IbkrAccountServiceError(
                    "IBKR returned no account summary for "
                    f"paper account {account_id}."
                )

            cash_item = account_values.get("TotalCashValue")
            buying_power_item = account_values.get("BuyingPower")

            cash = self._parse_required_number(
                cash_item,
                tag="TotalCashValue",
                account_id=account_id,
            )

            buying_power = self._parse_required_number(
                buying_power_item,
                tag="BuyingPower",
                account_id=account_id,
            )

            currency = self._resolve_currency(
                account_values,
                account_id=account_id,
            )

            return BrokerAccount(
                broker_name="IBKR",
                account_id=account_id,
                cash=cash,
                buying_power=buying_power,
                currency=currency,
                status="ACTIVE",
            )

        finally:
            if request_started:
                self._client.cancelAccountSummary(
                    self._client.ACCOUNT_SUMMARY_REQUEST_ID
                )

    def read_positions(self) -> tuple[BrokerPosition, ...]:
        self._require_connected()

        account_id = self._require_selected_account()

        self._client.positions_ready.clear()
        self._client.positions = []
        self._clear_errors()

        request_started = False

        try:
            self._client.reqPositions()
            request_started = True

            self._wait_for_event(
                self._client.positions_ready,
                description="position list",
            )

            self._raise_if_errors("reading positions")

            unexpected_accounts = sorted(
                {
                    position.account_id
                    for position in self._client.positions
                    if position.account_id != account_id
                }
            )

            if unexpected_accounts:
                raise IbkrAccountServiceError(
                    "IBKR returned positions for unexpected "
                    "account(s): "
                    + ", ".join(unexpected_accounts)
                )

            return tuple(
                position
                for position in self._client.positions
                if position.account_id == account_id
            )

        finally:
            if request_started:
                self._client.cancelPositions()

    def disconnect(self) -> None:
        if self._client.isConnected():
            self._client.disconnect()

        if self._network_thread is not None:
            self._network_thread.join(timeout=2.0)
            self._network_thread = None

        self._selected_account_id = None

    def _select_paper_account(self) -> str:
        accounts = [
            account.strip().upper()
            for account in self._client.managed_accounts
            if account.strip()
        ]

        paper_accounts = list(
            dict.fromkeys(
                account
                for account in accounts
                if account.startswith("DU")
            )
        )

        if self.expected_account_id is not None:
            if self.expected_account_id not in paper_accounts:
                raise IbkrAccountServiceError(
                    "Configured IBKR Paper account "
                    f"{self.expected_account_id} was not returned "
                    "by TWS."
                )

            return self.expected_account_id

        if not paper_accounts:
            raise IbkrAccountServiceError(
                "No DU-prefixed IBKR Paper account was returned "
                "by TWS."
            )

        if len(paper_accounts) > 1:
            raise IbkrAccountServiceError(
                "Multiple IBKR Paper accounts were returned. "
                "Configure expected_account_id explicitly."
            )

        return paper_accounts[0]

    def _wait_for_event(
        self,
        event: threading.Event,
        *,
        description: str,
    ) -> None:
        if not event.wait(self.timeout_seconds):
            raise IbkrAccountServiceError(
                f"Timeout while waiting for {description}."
            )

    def _raise_if_errors(self, operation: str) -> None:
        if not self._client.errors:
            return

        messages = [
            (
                f"reqId={error.request_id}, "
                f"code={error.error_code}, "
                f"message={error.message}"
            )
            for error in self._client.errors
        ]

        raise IbkrAccountServiceError(
            f"IBKR API error while {operation}: "
            + " | ".join(messages)
        )

    def _parse_required_number(
        self,
        item: _RawAccountValue | None,
        *,
        tag: str,
        account_id: str,
    ) -> float:
        if item is None or not item.value:
            raise IbkrAccountServiceError(
                f"{tag} was not returned for account {account_id}."
            )

        try:
            value = float(item.value)
        except (TypeError, ValueError) as exc:
            raise IbkrAccountServiceError(
                f"{tag} contained an invalid numeric value "
                f"for account {account_id}: {item.value!r}."
            ) from exc

        if not math.isfinite(value):
            raise IbkrAccountServiceError(
                f"{tag} contained a non-finite value "
                f"for account {account_id}."
            )

        return value

    def _resolve_currency(
        self,
        account_values: dict[str, _RawAccountValue],
        *,
        account_id: str,
    ) -> str:
        candidates: list[str] = []

        currency_tag = account_values.get("Currency")
        cash_item = account_values.get("TotalCashValue")
        buying_power_item = account_values.get("BuyingPower")

        if currency_tag is not None:
            if currency_tag.value:
                candidates.append(currency_tag.value.upper())
            if currency_tag.currency:
                candidates.append(currency_tag.currency.upper())

        if cash_item is not None and cash_item.currency:
            candidates.append(cash_item.currency.upper())

        if buying_power_item is not None and buying_power_item.currency:
            candidates.append(buying_power_item.currency.upper())

        currencies = {
            currency.strip()
            for currency in candidates
            if currency.strip() and currency.strip() != "BASE"
        }

        if not currencies:
            raise IbkrAccountServiceError(
                "No account currency was returned for "
                f"account {account_id}."
            )

        if len(currencies) > 1:
            raise IbkrAccountServiceError(
                "Conflicting account currencies were returned for "
                f"account {account_id}: "
                + ", ".join(sorted(currencies))
            )

        return next(iter(currencies))

    def _require_connected(self) -> None:
        if not self.is_connected:
            raise IbkrAccountServiceError(
                "IBKR account service is not connected."
            )

    def _require_selected_account(self) -> str:
        if self._selected_account_id is None:
            raise IbkrAccountServiceError(
                "No IBKR Paper account has been selected."
            )

        return self._selected_account_id

    def _clear_errors(self) -> None:
        self._client.errors = []

    def _reset_connection_state(self) -> None:
        self._client.connection_ready.clear()
        self._client.accounts_ready.clear()
        self._client.next_order_id = None
        self._client.managed_accounts = []
        self._clear_errors()

    def __enter__(self) -> IbkrAccountService:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()