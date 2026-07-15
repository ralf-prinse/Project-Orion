from __future__ import annotations

import math
import threading
import time
from datetime import datetime

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import ExecutionFilter
from ibapi.order import Order as IbkrOrder
from ibapi.wrapper import EWrapper

from services.ibkr.ibkr_broker import IbkrOrderOutcome


class IbkrOrderTransportError(RuntimeError):
    """Raised when an IBKR order operation cannot finish safely."""


class _IbkrOrderClient(EWrapper, EClient):
    INFORMATIONAL_ERROR_CODES = {2104, 2106, 2107, 2108, 2158}
    CANCELLED_STATUSES = {"APICANCELLED", "CANCELLED"}
    REJECTED_STATUSES = {"INACTIVE"}
    EXECUTION_RECONCILIATION_REQUEST_ID = 9101

    def __init__(self) -> None:
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.connection_ready = threading.Event()
        self.accounts_ready = threading.Event()
        self.terminal_event = threading.Event()
        self.execution_reconciliation_ready = threading.Event()

        self.next_order_id: int | None = None
        self.active_order_id: int | None = None
        self.expected_quantity: int = 0
        self.managed_accounts: list[str] = []
        self.outcome: IbkrOrderOutcome | None = None
        self.errors: list[str] = []

        self._execution_ids: set[str] = set()
        self._filled_quantity = 0.0
        self._fill_value = 0.0
        self._last_fill_time: datetime | None = None

    def reset_connection_state(self) -> None:
        self.connection_ready.clear()
        self.accounts_ready.clear()
        self.execution_reconciliation_ready.clear()
        self.next_order_id = None
        self.managed_accounts = []
        self.errors = []

    def reset_order_state(self, order_id: int, expected_quantity: int) -> None:
        self.active_order_id = int(order_id)
        self.expected_quantity = int(expected_quantity)
        self.outcome = None
        self.errors = []
        self.terminal_event.clear()
        self.execution_reconciliation_ready.clear()
        self._execution_ids = set()
        self._filled_quantity = 0.0
        self._fill_value = 0.0
        self._last_fill_time = None

    def nextValidId(self, orderId: int) -> None:
        self.next_order_id = int(orderId)
        self.connection_ready.set()

    def managedAccounts(self, accountsList: str) -> None:
        accounts = [
            account.strip().upper()
            for account in str(accountsList).split(",")
            if account.strip()
        ]
        self.managed_accounts = list(dict.fromkeys(accounts))
        self.accounts_ready.set()

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ) -> None:
        if self.active_order_id is None or int(orderId) != self.active_order_id:
            return

        normalized_status = str(status).strip().upper()
        filled_quantity = self._safe_quantity(filled)
        average_fill_price = self._safe_float(avgFillPrice)

        if normalized_status == "FILLED":
            self.outcome = IbkrOrderOutcome(
                status="FILLED",
                filled_quantity=filled_quantity,
                average_fill_price=average_fill_price,
                filled_at=datetime.now(),
                message="IBKR Paper order filled via orderStatus.",
            )
            self.terminal_event.set()
            return

        if normalized_status in self.CANCELLED_STATUSES:
            self.outcome = IbkrOrderOutcome(
                status="CANCELLED",
                filled_quantity=filled_quantity,
                average_fill_price=average_fill_price,
                message=f"IBKR order ended with status {normalized_status}.",
            )
            self.terminal_event.set()
            return

        if normalized_status in self.REJECTED_STATUSES:
            self.outcome = IbkrOrderOutcome(
                status="REJECTED",
                filled_quantity=filled_quantity,
                average_fill_price=average_fill_price,
                message=f"IBKR order ended with status {normalized_status}.",
            )
            self.terminal_event.set()

    def execDetails(self, reqId, contract, execution) -> None:
        if self.active_order_id is None:
            return

        try:
            execution_order_id = int(execution.orderId)
        except (TypeError, ValueError):
            return

        if execution_order_id != self.active_order_id:
            return

        execution_id = str(getattr(execution, "execId", "")).strip()
        if execution_id and execution_id in self._execution_ids:
            return
        if execution_id:
            self._execution_ids.add(execution_id)

        shares = self._safe_float(getattr(execution, "shares", 0))
        price = self._safe_float(getattr(execution, "price", 0))
        if not math.isfinite(shares) or not math.isfinite(price):
            return
        if shares <= 0 or price <= 0:
            return

        self._filled_quantity += shares
        self._fill_value += shares * price
        self._last_fill_time = self._parse_execution_time(
            str(getattr(execution, "time", ""))
        ) or datetime.now()

        if self._filled_quantity + 1e-9 >= self.expected_quantity:
            average_price = self._fill_value / self._filled_quantity
            self.outcome = IbkrOrderOutcome(
                status="FILLED",
                filled_quantity=int(round(self._filled_quantity)),
                average_fill_price=average_price,
                filled_at=self._last_fill_time,
                message="IBKR Paper order filled via execDetails.",
            )
            self.terminal_event.set()

    def execDetailsEnd(self, reqId: int) -> None:
        if int(reqId) == self.EXECUTION_RECONCILIATION_REQUEST_ID:
            self.execution_reconciliation_ready.set()

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

        message = f"reqId={reqId}, code={error_code}, message={errorString}"
        advanced_reject = str(advancedOrderRejectJson or "").strip()
        if advanced_reject:
            message += ", advanced_reject=" + advanced_reject
        self.errors.append(message)

        if (
            self.active_order_id is not None
            and int(reqId) in {-1, self.active_order_id}
        ):
            self.outcome = IbkrOrderOutcome(status="REJECTED", message=message)
            self.terminal_event.set()

    @staticmethod
    def _safe_float(value) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @classmethod
    def _safe_quantity(cls, value) -> int:
        return int(round(cls._safe_float(value)))

    @staticmethod
    def _parse_execution_time(value: str) -> datetime | None:
        normalized = value.strip()
        if not normalized:
            return None
        for format_string in (
            "%Y%m%d %H:%M:%S %Z",
            "%Y%m%d %H:%M:%S",
            "%Y%m%d-%H:%M:%S",
        ):
            try:
                return datetime.strptime(normalized, format_string)
            except ValueError:
                continue
        return None


class IbkrOrderTransport:
    """Technical transport for one controlled TWS Paper order at a time."""

    PAPER_PORT = 7497

    def __init__(
        self,
        *,
        paper_account_id: str,
        host: str = "127.0.0.1",
        port: int = PAPER_PORT,
        client_id: int = 120,
        connection_timeout_seconds: float = 15.0,
        reconciliation_timeout_seconds: float = 5.0,
        allow_order_submission: bool = False,
        disconnect_after_order: bool = True,
        client: _IbkrOrderClient | None = None,
    ) -> None:
        normalized_account_id = paper_account_id.strip().upper()
        if not normalized_account_id.startswith("DU"):
            raise ValueError(
                "paper_account_id must be an IBKR Paper account starting with 'DU'."
            )
        if not host.strip():
            raise ValueError("IBKR host must not be empty.")
        if int(port) != self.PAPER_PORT:
            raise ValueError(
                "IbkrOrderTransport accepts only TWS Paper port 7497."
            )
        if connection_timeout_seconds <= 0:
            raise ValueError(
                "connection_timeout_seconds must be greater than zero."
            )
        if reconciliation_timeout_seconds <= 0:
            raise ValueError(
                "reconciliation_timeout_seconds must be greater than zero."
            )

        self.paper_account_id = normalized_account_id
        self.host = host.strip()
        self.port = int(port)
        self.client_id = int(client_id)
        self.connection_timeout_seconds = float(connection_timeout_seconds)
        self.reconciliation_timeout_seconds = float(
            reconciliation_timeout_seconds
        )
        self.allow_order_submission = bool(allow_order_submission)
        self.disconnect_after_order = bool(disconnect_after_order)

        self._client = client or _IbkrOrderClient()
        self._network_thread: threading.Thread | None = None
        self._submission_lock = threading.Lock()
        self._verified_account_id: str | None = None

    @property
    def is_connected(self) -> bool:
        return bool(self._client.isConnected())

    @property
    def verified_account_id(self) -> str | None:
        return self._verified_account_id

    def submit_order(
        self,
        *,
        contract: Contract,
        order: IbkrOrder,
        timeout_seconds: float,
    ) -> IbkrOrderOutcome:
        if not self.allow_order_submission:
            raise PermissionError(
                "IBKR order submission is disabled. Set "
                "allow_order_submission=True only for an explicitly "
                "controlled TWS Paper-order test."
            )
        if timeout_seconds <= 0:
            raise ValueError("Order timeout_seconds must be greater than zero.")

        self._validate_contract(contract)
        expected_quantity = self._validate_ibkr_order(order)

        with self._submission_lock:
            try:
                self._connect()
                order_id = self._claim_order_id()
                order.account = self.paper_account_id
                self._client.reset_order_state(order_id, expected_quantity)
                self._client.placeOrder(order_id, contract, order)

                if self._client.terminal_event.wait(float(timeout_seconds)):
                    return self._require_outcome()

                reconciled = self._reconcile_execution()
                if reconciled is not None:
                    return reconciled

                self._cancel_order_safely(order_id)
                raise TimeoutError(
                    "Timed out without a terminal IBKR status or confirmed "
                    f"execution for order {order_id}. The order was cancelled "
                    "after execution reconciliation. Verify TWS before retrying."
                )
            finally:
                if self.disconnect_after_order:
                    self.disconnect()

    def disconnect(self) -> None:
        if self._client.isConnected():
            self._client.disconnect()
        if self._network_thread is not None:
            self._network_thread.join(timeout=2.0)
            self._network_thread = None
        self._verified_account_id = None

    def _connect(self) -> None:
        if self.is_connected:
            if self._client.next_order_id is None:
                raise IbkrOrderTransportError(
                    "IBKR transport is connected but has no valid next order ID."
                )
            if self._verified_account_id != self.paper_account_id:
                self._verify_managed_account()
            return

        self._verified_account_id = None
        self._client.reset_connection_state()
        try:
            self._client.connect(self.host, self.port, clientId=self.client_id)
            self._network_thread = threading.Thread(
                target=self._client.run,
                name="ibkr-order-transport",
                daemon=True,
            )
            self._network_thread.start()

            if not self._client.connection_ready.wait(
                self.connection_timeout_seconds
            ):
                raise IbkrOrderTransportError(
                    "Timeout while waiting for TWS order connection readiness."
                )
            if self._client.next_order_id is None:
                raise IbkrOrderTransportError(
                    "TWS connection became ready without a valid next order ID."
                )
            self._raise_connection_errors()
            self._verify_managed_account()
        except Exception:
            self.disconnect()
            raise

    def _verify_managed_account(self) -> None:
        self._client.accounts_ready.clear()
        self._client.managed_accounts = []
        self._client.reqManagedAccts()

        if not self._client.accounts_ready.wait(self.connection_timeout_seconds):
            raise IbkrOrderTransportError(
                "Timeout while waiting for IBKR managed accounts."
            )
        self._raise_connection_errors()

        returned_accounts = {
            account.strip().upper()
            for account in self._client.managed_accounts
            if account.strip()
        }
        paper_accounts = {
            account for account in returned_accounts if account.startswith("DU")
        }
        if self.paper_account_id not in paper_accounts:
            description = ", ".join(sorted(returned_accounts)) or "none"
            raise IbkrOrderTransportError(
                f"Configured IBKR Paper account {self.paper_account_id} was "
                "not returned by the connected TWS session. Returned "
                f"accounts: {description}."
            )
        self._verified_account_id = self.paper_account_id

    def _reconcile_execution(self) -> IbkrOrderOutcome | None:
        self._client.execution_reconciliation_ready.clear()
        execution_filter = ExecutionFilter()
        execution_filter.acctCode = self.paper_account_id
        self._client.reqExecutions(
            self._client.EXECUTION_RECONCILIATION_REQUEST_ID,
            execution_filter,
        )

        deadline_reached = not self._client.execution_reconciliation_ready.wait(
            self.reconciliation_timeout_seconds
        )
        if self._client.terminal_event.is_set():
            return self._require_outcome()
        if deadline_reached:
            return None
        return self._client.outcome

    def _require_outcome(self) -> IbkrOrderOutcome:
        outcome = self._client.outcome
        if outcome is None:
            raise IbkrOrderTransportError(
                "IBKR signalled terminal order completion without an outcome."
            )
        return outcome

    def _raise_connection_errors(self) -> None:
        if self._client.errors:
            raise IbkrOrderTransportError(
                "IBKR API error while connecting: "
                + " | ".join(self._client.errors)
            )

    def _claim_order_id(self) -> int:
        next_order_id = self._client.next_order_id
        if next_order_id is None:
            raise IbkrOrderTransportError("No valid IBKR order ID is available.")
        claimed_order_id = int(next_order_id)
        self._client.next_order_id = claimed_order_id + 1
        return claimed_order_id

    def _validate_contract(self, contract: Contract) -> None:
        symbol = str(contract.symbol).strip().upper()
        security_type = str(contract.secType).strip().upper()
        exchange = str(contract.exchange).strip().upper()
        currency = str(contract.currency).strip().upper()

        if not symbol:
            raise ValueError("IBKR contract symbol must not be empty.")
        if security_type != "STK":
            raise ValueError(
                "IbkrOrderTransport currently supports only STK contracts."
            )
        if exchange != "SMART":
            raise ValueError(
                "IbkrOrderTransport currently supports only SMART routing."
            )
        if not currency:
            raise ValueError("IBKR contract currency must not be empty.")

    def _validate_ibkr_order(self, order: IbkrOrder) -> int:
        action = str(order.action).strip().upper()
        order_type = str(order.orderType).strip().upper()
        try:
            quantity = float(order.totalQuantity)
        except (TypeError, ValueError) as exc:
            raise ValueError("IBKR order quantity must be numeric.") from exc

        if action != "BUY":
            raise ValueError(
                "IbkrOrderTransport currently supports only BUY orders."
            )
        if order_type != "MKT":
            raise ValueError(
                "IbkrOrderTransport currently supports only MKT orders."
            )
        if not math.isfinite(quantity):
            raise ValueError("IBKR order quantity must be finite.")
        if quantity <= 0:
            raise ValueError("IBKR order quantity must be greater than zero.")
        if not quantity.is_integer():
            raise ValueError("IBKR order quantity must be a whole number.")
        if not bool(order.transmit):
            raise ValueError(
                "Controlled IBKR Paper orders must explicitly set transmit=True."
            )
        return int(quantity)

    def _cancel_order_safely(self, order_id: int) -> None:
        try:
            self._client.cancelOrder(order_id, "")
        except TypeError:
            self._client.cancelOrder(order_id)
        except Exception:
            pass

    def __enter__(self) -> IbkrOrderTransport:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.disconnect()