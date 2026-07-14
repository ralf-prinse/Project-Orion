from __future__ import annotations

import math
import threading
from datetime import datetime

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order as IbkrOrder
from ibapi.wrapper import EWrapper

from services.ibkr.ibkr_broker import IbkrOrderOutcome


class IbkrOrderTransportError(RuntimeError):
    """
    Raised when the IBKR order transport cannot safely complete an
    order operation.
    """


class _IbkrOrderClient(EWrapper, EClient):
    """
    Low-level callback client used only by IbkrOrderTransport.

    It owns IBKR network callbacks but does not own Orion trading,
    risk, portfolio or position lifecycle state.
    """

    INFORMATIONAL_ERROR_CODES = {
        2104,
        2106,
        2107,
        2108,
        2158,
    }

    CANCELLED_STATUSES = {
        "APICANCELLED",
        "CANCELLED",
    }

    REJECTED_STATUSES = {
        "INACTIVE",
    }

    def __init__(self) -> None:
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.connection_ready = threading.Event()
        self.terminal_event = threading.Event()

        self.next_order_id: int | None = None
        self.active_order_id: int | None = None
        self.outcome: IbkrOrderOutcome | None = None

        self.errors: list[str] = []

    def reset_order_state(
        self,
        order_id: int,
    ) -> None:
        self.active_order_id = int(order_id)
        self.outcome = None
        self.errors = []
        self.terminal_event.clear()

    def nextValidId(
        self,
        orderId: int,
    ) -> None:
        self.next_order_id = int(orderId)
        self.connection_ready.set()

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
        if self.active_order_id is None:
            return

        if int(orderId) != self.active_order_id:
            return

        normalized_status = str(status).strip().upper()

        try:
            filled_quantity = int(
                round(float(filled))
            )
        except (TypeError, ValueError):
            filled_quantity = 0

        try:
            average_fill_price = float(avgFillPrice)
        except (TypeError, ValueError):
            average_fill_price = 0.0

        if normalized_status == "FILLED":
            self.outcome = IbkrOrderOutcome(
                status="FILLED",
                filled_quantity=filled_quantity,
                average_fill_price=average_fill_price,
                filled_at=datetime.now(),
                message="IBKR Paper order filled.",
            )
            self.terminal_event.set()
            return

        if normalized_status in self.CANCELLED_STATUSES:
            self.outcome = IbkrOrderOutcome(
                status="CANCELLED",
                filled_quantity=filled_quantity,
                average_fill_price=average_fill_price,
                message=(
                    "IBKR order ended with status "
                    f"{normalized_status}."
                ),
            )
            self.terminal_event.set()
            return

        if normalized_status in self.REJECTED_STATUSES:
            self.outcome = IbkrOrderOutcome(
                status="REJECTED",
                filled_quantity=filled_quantity,
                average_fill_price=average_fill_price,
                message=(
                    "IBKR order ended with status "
                    f"{normalized_status}."
                ),
            )
            self.terminal_event.set()

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

        message = (
            f"reqId={reqId}, "
            f"code={error_code}, "
            f"message={errorString}"
        )

        advanced_reject = str(
            advancedOrderRejectJson or ""
        ).strip()

        if advanced_reject:
            message += (
                ", advanced_reject="
                + advanced_reject
            )

        self.errors.append(message)

        if (
            self.active_order_id is not None
            and int(reqId) in {
                -1,
                self.active_order_id,
            }
        ):
            self.outcome = IbkrOrderOutcome(
                status="REJECTED",
                message=message,
            )
            self.terminal_event.set()


class IbkrOrderTransport:
    """
    Technical TWS Paper order transport for IbkrBroker.

    Safety rules:
    - only TWS Paper port 7497 is accepted;
    - only DU-prefixed Paper accounts are accepted;
    - order submission is disabled by default;
    - one order is handled at a time;
    - every operation has a bounded timeout;
    - the transport disconnects cleanly by default.

    This class makes no trading decisions and does not mutate Orion
    portfolio or lifecycle state.
    """

    PAPER_PORT = 7497

    def __init__(
        self,
        *,
        paper_account_id: str,
        host: str = "127.0.0.1",
        port: int = PAPER_PORT,
        client_id: int = 120,
        connection_timeout_seconds: float = 15.0,
        allow_order_submission: bool = False,
        disconnect_after_order: bool = True,
        client: _IbkrOrderClient | None = None,
    ) -> None:
        normalized_account_id = (
            paper_account_id.strip().upper()
        )

        if not normalized_account_id.startswith("DU"):
            raise ValueError(
                "paper_account_id must be an IBKR Paper "
                "account starting with 'DU'."
            )

        if not host.strip():
            raise ValueError(
                "IBKR host must not be empty."
            )

        if int(port) != self.PAPER_PORT:
            raise ValueError(
                "IbkrOrderTransport accepts only TWS Paper "
                "port 7497."
            )

        if connection_timeout_seconds <= 0:
            raise ValueError(
                "connection_timeout_seconds must be greater "
                "than zero."
            )

        self.paper_account_id = normalized_account_id
        self.host = host.strip()
        self.port = int(port)
        self.client_id = int(client_id)
        self.connection_timeout_seconds = float(
            connection_timeout_seconds
        )
        self.allow_order_submission = bool(
            allow_order_submission
        )
        self.disconnect_after_order = bool(
            disconnect_after_order
        )

        self._client = client or _IbkrOrderClient()
        self._network_thread: threading.Thread | None = None
        self._submission_lock = threading.Lock()

    @property
    def is_connected(self) -> bool:
        return bool(
            self._client.isConnected()
        )

    def submit_order(
        self,
        *,
        contract: Contract,
        order: IbkrOrder,
        timeout_seconds: float,
    ) -> IbkrOrderOutcome:
        """
        Submit one order and wait for a terminal broker outcome.

        This method is blocked unless allow_order_submission=True was
        explicitly supplied when creating the transport.
        """

        if not self.allow_order_submission:
            raise PermissionError(
                "IBKR order submission is disabled. "
                "Set allow_order_submission=True only for an "
                "explicitly controlled TWS Paper-order test."
            )

        if timeout_seconds <= 0:
            raise ValueError(
                "Order timeout_seconds must be greater than zero."
            )

        self._validate_contract(contract)
        self._validate_ibkr_order(order)

        with self._submission_lock:
            try:
                self._connect()

                order_id = self._claim_order_id()

                order.account = self.paper_account_id

                self._client.reset_order_state(
                    order_id
                )

                self._client.placeOrder(
                    order_id,
                    contract,
                    order,
                )

                if not self._client.terminal_event.wait(
                    float(timeout_seconds)
                ):
                    self._cancel_order_safely(
                        order_id
                    )

                    raise TimeoutError(
                        "Timed out waiting for terminal "
                        f"IBKR order status for order {order_id}."
                    )

                outcome = self._client.outcome

                if outcome is None:
                    raise IbkrOrderTransportError(
                        "IBKR signalled terminal order completion "
                        "without an outcome."
                    )

                return outcome

            finally:
                if self.disconnect_after_order:
                    self.disconnect()

    def disconnect(self) -> None:
        if self._client.isConnected():
            self._client.disconnect()

        if self._network_thread is not None:
            self._network_thread.join(
                timeout=2.0
            )
            self._network_thread = None

    def _connect(self) -> None:
        if self.is_connected:
            if self._client.next_order_id is None:
                raise IbkrOrderTransportError(
                    "IBKR transport is connected but has no "
                    "valid next order ID."
                )
            return

        self._client.connection_ready.clear()
        self._client.next_order_id = None
        self._client.errors = []

        try:
            self._client.connect(
                self.host,
                self.port,
                clientId=self.client_id,
            )

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
                    "Timeout while waiting for TWS order "
                    "connection readiness."
                )

            if self._client.next_order_id is None:
                raise IbkrOrderTransportError(
                    "TWS connection became ready without a "
                    "valid next order ID."
                )

            if self._client.errors:
                raise IbkrOrderTransportError(
                    "IBKR API error while connecting: "
                    + " | ".join(
                        self._client.errors
                    )
                )

        except Exception:
            self.disconnect()
            raise

    def _claim_order_id(self) -> int:
        next_order_id = self._client.next_order_id

        if next_order_id is None:
            raise IbkrOrderTransportError(
                "No valid IBKR order ID is available."
            )

        claimed_order_id = int(
            next_order_id
        )

        self._client.next_order_id = (
            claimed_order_id + 1
        )

        return claimed_order_id

    def _validate_contract(
        self,
        contract: Contract,
    ) -> None:
        symbol = str(
            contract.symbol
        ).strip().upper()

        security_type = str(
            contract.secType
        ).strip().upper()

        exchange = str(
            contract.exchange
        ).strip().upper()

        currency = str(
            contract.currency
        ).strip().upper()

        if not symbol:
            raise ValueError(
                "IBKR contract symbol must not be empty."
            )

        if security_type != "STK":
            raise ValueError(
                "IbkrOrderTransport currently supports only "
                "STK contracts."
            )

        if exchange != "SMART":
            raise ValueError(
                "IbkrOrderTransport currently supports only "
                "SMART routing."
            )

        if not currency:
            raise ValueError(
                "IBKR contract currency must not be empty."
            )

    def _validate_ibkr_order(
        self,
        order: IbkrOrder,
    ) -> None:
        action = str(
            order.action
        ).strip().upper()

        order_type = str(
            order.orderType
        ).strip().upper()

        try:
            quantity = float(
                order.totalQuantity
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "IBKR order quantity must be numeric."
            ) from exc

        if action != "BUY":
            raise ValueError(
                "IbkrOrderTransport currently supports only "
                "BUY orders."
            )

        if order_type != "MKT":
            raise ValueError(
                "IbkrOrderTransport currently supports only "
                "MKT orders."
            )

        if not math.isfinite(quantity):
            raise ValueError(
                "IBKR order quantity must be finite."
            )

        if quantity <= 0:
            raise ValueError(
                "IBKR order quantity must be greater than zero."
            )

        if not bool(order.transmit):
            raise ValueError(
                "Controlled IBKR Paper orders must explicitly "
                "set transmit=True."
            )

    def _cancel_order_safely(
        self,
        order_id: int,
    ) -> None:
        try:
            self._client.cancelOrder(
                order_id,
                "",
            )
        except TypeError:
            self._client.cancelOrder(
                order_id
            )
        except Exception:
            pass

    def __enter__(self) -> IbkrOrderTransport:
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.disconnect()