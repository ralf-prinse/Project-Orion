from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ibapi.contract import Contract
from ibapi.order import Order as IbkrOrder

from models.execution_result import ExecutionResult
from models.order import Order


class IbkrBrokerTransport(Protocol):
    """
    Minimal transport used by IbkrBroker.

    The production TWS transport will be implemented separately.
    Unit tests can inject a fake transport, so no real order is sent.
    """

    def submit_order(
        self,
        *,
        contract: Contract,
        order: IbkrOrder,
        timeout_seconds: float,
    ) -> "IbkrOrderOutcome":
        ...


@dataclass(frozen=True)
class IbkrOrderOutcome:
    """
    Terminal result returned by the IBKR transport.

    Only a complete fill may be mapped to an accepted Orion execution.
    """

    status: str
    filled_quantity: int = 0
    average_fill_price: float = 0.0
    filled_at: datetime | None = None
    message: str = ""


class IbkrBroker:
    """
    Interactive Brokers execution adapter.

    This class preserves the same practical interface as PaperBroker:

        execute(order: Order) -> ExecutionResult

    The broker does not own trading decisions, risk, portfolio state or
    position lifecycle. Those responsibilities remain elsewhere in Orion.

    A transport must be injected. This prevents accidental real order
    submission before the controlled IBKR Paper-order milestone.
    """

    SUPPORTED_SIDES = {"BUY", "SELL"}
    SUPPORTED_ORDER_TYPES = {"MARKET"}

    def __init__(
        self,
        *,
        transport: IbkrBrokerTransport,
        timeout_seconds: float = 30.0,
        exchange: str = "SMART",
        currency: str = "USD",
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError(
                "IBKR timeout_seconds must be greater than zero."
            )

        if not exchange.strip():
            raise ValueError("IBKR exchange must not be empty.")

        if not currency.strip():
            raise ValueError("IBKR currency must not be empty.")

        self.transport = transport
        self.timeout_seconds = float(timeout_seconds)
        self.exchange = exchange.strip().upper()
        self.currency = currency.strip().upper()

    def execute(self, order: Order) -> ExecutionResult:
        validation_error = self._validate_order(order)

        if validation_error is not None:
            return ExecutionResult(
                accepted=False,
                status="REJECTED",
                order=order,
                message=validation_error,
            )

        contract = self._build_contract(order)
        ibkr_order = self._build_ibkr_order(order)

        try:
            outcome = self.transport.submit_order(
                contract=contract,
                order=ibkr_order,
                timeout_seconds=self.timeout_seconds,
            )
        except TimeoutError as exc:
            return ExecutionResult(
                accepted=False,
                status="TIMEOUT",
                order=order,
                message=str(exc) or "IBKR order timed out.",
            )
        except Exception as exc:
            return ExecutionResult(
                accepted=False,
                status="ERROR",
                order=order,
                message=f"IBKR order submission failed: {exc}",
            )

        return self._map_outcome(
            original_order=order,
            outcome=outcome,
        )

    def _validate_order(self, order: Order) -> str | None:
        symbol = order.symbol.strip().upper()
        side = order.side.strip().upper()
        order_type = order.order_type.strip().upper()

        if not symbol:
            return "Order symbol must not be empty."

        if side not in self.SUPPORTED_SIDES:
            return (
                "IbkrBroker supports only BUY and SELL orders. "
                f"Received: {order.side!r}."
            )

        if order_type not in self.SUPPORTED_ORDER_TYPES:
            return (
                "IbkrBroker currently supports only MARKET orders. "
                f"Received: {order.order_type!r}."
            )

        if order.quantity <= 0:
            return "Order quantity must be greater than zero."

        if not isinstance(order.quantity, int):
            return "Order quantity must be an integer."

        try:
            price = float(order.price)
        except (TypeError, ValueError):
            return "Order price must be numeric."

        if not math.isfinite(price):
            return "Order price must be finite."

        if price <= 0:
            return "Order price must be greater than zero."

        return None

    def _build_contract(self, order: Order) -> Contract:
        contract = Contract()
        contract.symbol = order.symbol.strip().upper()
        contract.secType = "STK"
        contract.exchange = self.exchange
        contract.currency = self.currency
        return contract

    def _build_ibkr_order(self, order: Order) -> IbkrOrder:
        ibkr_order = IbkrOrder()
        ibkr_order.action = order.side.strip().upper()
        ibkr_order.orderType = "MKT"
        ibkr_order.totalQuantity = int(order.quantity)

        # Disable legacy attributes rejected by newer TWS versions
        # for normal SMART-routed stock orders.
        ibkr_order.eTradeOnly = False
        ibkr_order.firmQuoteOnly = False

        ibkr_order.transmit = True
        return ibkr_order

    def _map_outcome(
        self,
        *,
        original_order: Order,
        outcome: IbkrOrderOutcome,
    ) -> ExecutionResult:
        status = outcome.status.strip().upper()

        if status != "FILLED":
            return ExecutionResult(
                accepted=False,
                status=status or "ERROR",
                order=original_order,
                message=(
                    outcome.message
                    or f"IBKR order ended with status {status or 'ERROR'}."
                ),
            )

        if outcome.filled_quantity != original_order.quantity:
            return ExecutionResult(
                accepted=False,
                status="PARTIAL_FILL",
                order=original_order,
                message=(
                    "IBKR order was not completely filled. "
                    f"Expected {original_order.quantity}, "
                    f"received {outcome.filled_quantity}."
                ),
            )

        if outcome.filled_quantity <= 0:
            return ExecutionResult(
                accepted=False,
                status="ERROR",
                order=original_order,
                message="IBKR reported a fill with zero quantity.",
            )

        if not math.isfinite(outcome.average_fill_price):
            return ExecutionResult(
                accepted=False,
                status="ERROR",
                order=original_order,
                message="IBKR reported a non-finite fill price.",
            )

        if outcome.average_fill_price <= 0:
            return ExecutionResult(
                accepted=False,
                status="ERROR",
                order=original_order,
                message="IBKR reported an invalid fill price.",
            )

        return ExecutionResult(
            accepted=True,
            status="FILLED",
            order=original_order,
            message=outcome.message or "IBKR Paper order filled.",
            executed_price=outcome.average_fill_price,
            executed_quantity=outcome.filled_quantity,
            executed_at=outcome.filled_at or datetime.now(),
        )