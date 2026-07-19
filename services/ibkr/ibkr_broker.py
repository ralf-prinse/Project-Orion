from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ibapi.contract import Contract
from ibapi.order import Order as IbkrOrder

from models.execution_result import ExecutionResult
from models.order import Order
from services.ibkr.ibkr_stock_contract_factory import (
    IbkrStockContractFactory,
)
from services.execution_quality_gate import (
    ExecutionQualityGate,
    ExecutionQuote,
)


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

    def submit_bracket_order(
        self,
        *,
        contract: Contract,
        parent_order: IbkrOrder,
        take_profit_order: IbkrOrder,
        stop_loss_order: IbkrOrder,
        timeout_seconds: float,
    ) -> "IbkrOrderOutcome":
        ...


class IbkrExecutionQuoteProvider(Protocol):
    def get_quote(self, symbol: str) -> ExecutionQuote:
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
    order_id: int | None = None
    permanent_id: int | None = None
    child_order_ids: tuple[int, ...] = ()


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
        contract_factory: IbkrStockContractFactory | None = None,
        enable_native_protective_orders: bool = False,
        quote_provider: IbkrExecutionQuoteProvider | None = None,
        execution_quality_gate: ExecutionQualityGate | None = None,
        max_bid_ask_spread_pct: float = 0.003,
        max_quote_age_seconds: float = 5.0,
        max_entry_slippage_pct: float = 0.0015,
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
        self.contract_factory = (
            contract_factory or IbkrStockContractFactory()
        )
        self.enable_native_protective_orders = bool(
            enable_native_protective_orders
        )
        self.quote_provider = quote_provider
        self.execution_quality_gate = (
            execution_quality_gate or ExecutionQualityGate()
        )
        self.max_bid_ask_spread_pct = float(max_bid_ask_spread_pct)
        self.max_quote_age_seconds = float(max_quote_age_seconds)
        self.max_entry_slippage_pct = float(max_entry_slippage_pct)

    def execute(self, order: Order) -> ExecutionResult:
        validation_error = self._validate_order(order)

        if validation_error is not None:
            return ExecutionResult(
                accepted=False,
                status="REJECTED",
                order=order,
                message=validation_error,
            )

        limit_price = None
        if (
            self.quote_provider is not None
            and (
                order.side.strip().upper() == "BUY"
                or order.execution_urgency.strip().upper() == "NORMAL"
            )
        ):
            try:
                quote = self.quote_provider.get_quote(order.symbol)
                quality = self.execution_quality_gate.evaluate(
                    quote=quote,
                    side=order.side,
                    max_spread_pct=self.max_bid_ask_spread_pct,
                    max_quote_age_seconds=self.max_quote_age_seconds,
                    max_slippage_pct=self.max_entry_slippage_pct,
                    required_quantity=order.quantity,
                    planned_price=order.price,
                )
            except Exception as exc:
                return ExecutionResult(
                    accepted=False,
                    status="EXECUTION_QUALITY_REJECTED",
                    order=order,
                    message=f"Live IBKR execution quote unavailable: {exc}",
                )
            if not quality.allowed:
                return ExecutionResult(
                    accepted=False,
                    status="EXECUTION_QUALITY_REJECTED",
                    order=order,
                    message=quality.reason,
                )
            limit_price = quality.marketable_limit_price

        contract = self._build_contract(order)
        ibkr_order = self._build_ibkr_order(
            order,
            limit_price=limit_price,
        )

        try:
            if (
                self.enable_native_protective_orders
                and order.side.strip().upper() == "BUY"
            ):
                ibkr_order.transmit = False
                take_profit, stop_loss = (
                    self._build_protective_orders(order)
                )
                outcome = self.transport.submit_bracket_order(
                    contract=contract,
                    parent_order=ibkr_order,
                    take_profit_order=take_profit,
                    stop_loss_order=stop_loss,
                    timeout_seconds=self.timeout_seconds,
                )
            else:
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

        if self.enable_native_protective_orders and side == "BUY":
            try:
                stop_loss = float(order.stop_loss_price)
                take_profit = float(order.take_profit_price)
            except (TypeError, ValueError):
                return (
                    "Native protective BUY requires finite stop-loss "
                    "and take-profit prices."
                )
            if not math.isfinite(stop_loss) or not math.isfinite(take_profit):
                return (
                    "Native protective BUY requires finite stop-loss "
                    "and take-profit prices."
                )
            if stop_loss <= 0 or stop_loss >= price:
                return "Protective stop-loss must be below the BUY price."
            if take_profit <= price:
                return "Protective take-profit must be above the BUY price."

        return None

    def _build_contract(self, order: Order) -> Contract:
        contract = self.contract_factory.build(order.symbol)
        contract.exchange = self.exchange
        if not order.symbol.strip().upper().endswith((".AS", ".DE")):
            contract.currency = self.currency
        return contract

    def _build_ibkr_order(
        self,
        order: Order,
        *,
        limit_price: float | None = None,
    ) -> IbkrOrder:
        ibkr_order = IbkrOrder()
        ibkr_order.action = order.side.strip().upper()
        if limit_price is None:
            ibkr_order.orderType = "MKT"
        else:
            ibkr_order.orderType = "LMT"
            ibkr_order.lmtPrice = float(limit_price)
        ibkr_order.totalQuantity = int(order.quantity)
        if order.client_order_id.strip():
            ibkr_order.orderRef = order.client_order_id.strip()
        if (
            order.side.strip().upper() == "SELL"
            and order.oca_group.strip()
        ):
            ibkr_order.ocaGroup = order.oca_group.strip()
            ibkr_order.ocaType = 1

        # Disable legacy attributes rejected by newer TWS versions
        # for normal SMART-routed stock orders.
        ibkr_order.eTradeOnly = False
        ibkr_order.firmQuoteOnly = False

        ibkr_order.transmit = True
        return ibkr_order

    def _build_protective_orders(
        self,
        order: Order,
    ) -> tuple[IbkrOrder, IbkrOrder]:
        opposite_action = "SELL"

        take_profit = IbkrOrder()
        take_profit.action = opposite_action
        take_profit.orderType = "LMT"
        take_profit.totalQuantity = int(order.quantity)
        take_profit.lmtPrice = float(order.take_profit_price)
        take_profit.eTradeOnly = False
        take_profit.firmQuoteOnly = False
        take_profit.transmit = False

        stop_loss = IbkrOrder()
        stop_loss.action = opposite_action
        stop_loss.orderType = "STP"
        stop_loss.totalQuantity = int(order.quantity)
        stop_loss.auxPrice = float(order.stop_loss_price)
        stop_loss.eTradeOnly = False
        stop_loss.firmQuoteOnly = False
        stop_loss.transmit = True

        if order.client_order_id.strip():
            base_reference = order.client_order_id.strip()
            take_profit.orderRef = base_reference + ":TP"
            stop_loss.orderRef = base_reference + ":SL"
        if order.oca_group.strip():
            take_profit.ocaGroup = order.oca_group.strip()
            take_profit.ocaType = 1
            stop_loss.ocaGroup = order.oca_group.strip()
            stop_loss.ocaType = 1

        return take_profit, stop_loss

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
