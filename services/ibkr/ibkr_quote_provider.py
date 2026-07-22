from __future__ import annotations

import threading
from datetime import UTC, datetime

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from services.execution_quality_gate import ExecutionQuote
from services.ibkr.ibkr_stock_contract_factory import IbkrStockContractFactory


class IbkrQuoteProviderError(RuntimeError):
    pass


class _IbkrQuoteClient(EWrapper, EClient):
    INFORMATIONAL_CODES = {2104, 2106, 2107, 2108, 2158}

    def __init__(self) -> None:
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.connection_ready = threading.Event()
        self.quote_ready = threading.Event()
        self.bid: float | None = None
        self.ask: float | None = None
        self.bid_size = 0.0
        self.ask_size = 0.0
        self.received_at: datetime | None = None
        self.errors: list[str] = []

    def reset_quote_state(self) -> None:
        self.connection_ready.clear()
        self.quote_ready.clear()
        self.bid = None
        self.ask = None
        self.bid_size = 0.0
        self.ask_size = 0.0
        self.received_at = None
        self.errors = []

    def nextValidId(self, orderId: int) -> None:
        self.connection_ready.set()

    def tickPrice(self, reqId, tickType, price, attrib) -> None:
        if int(tickType) == 1 and float(price) > 0:
            self.bid = float(price)
        elif int(tickType) == 2 and float(price) > 0:
            self.ask = float(price)
        self._mark_ready()

    def tickSize(self, reqId, tickType, size) -> None:
        numeric = float(size)
        if int(tickType) == 0:
            self.bid_size = numeric
        elif int(tickType) == 3:
            self.ask_size = numeric
        self._mark_ready()

    def _mark_ready(self) -> None:
        if (
            self.bid is not None
            and self.ask is not None
            and self.bid_size > 0
            and self.ask_size > 0
        ):
            self.received_at = datetime.now(UTC)
            self.quote_ready.set()

    def error(
        self,
        reqId,
        errorCode,
        errorString,
        advancedOrderRejectJson="",
    ) -> None:
        code = int(errorCode)
        if code in self.INFORMATIONAL_CODES:
            return
        self.errors.append(
            f"reqId={reqId}, code={code}, message={errorString}"
        )


class IbkrQuoteProvider:
    """One-shot live top-of-book provider for execution validation."""

    REQUEST_ID = 9401
    PAPER_PORT = 7497

    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = PAPER_PORT,
        client_id: int = 140,
        timeout_seconds: float = 5.0,
        client: _IbkrQuoteClient | None = None,
        contract_factory: IbkrStockContractFactory | None = None,
    ) -> None:
        if int(port) != self.PAPER_PORT:
            raise ValueError("IbkrQuoteProvider accepts only Paper port 7497.")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero.")
        self.host = host
        self.port = int(port)
        self.client_id = int(client_id)
        self.timeout_seconds = float(timeout_seconds)
        self.client = client or _IbkrQuoteClient()
        self.contract_factory = contract_factory or IbkrStockContractFactory()

    def get_quote(self, symbol: str) -> ExecutionQuote:
        client = self.client
        client.reset_quote_state()
        network_thread: threading.Thread | None = None
        try:
            client.connect(self.host, self.port, clientId=self.client_id)
            network_thread = threading.Thread(
                target=client.run,
                name="ibkr-execution-quote",
                daemon=True,
            )
            network_thread.start()
            if not client.connection_ready.wait(self.timeout_seconds):
                raise IbkrQuoteProviderError(
                    "Timeout waiting for TWS quote connection readiness."
                )

            contract = self.contract_factory.build(symbol)
            client.reqMarketDataType(1)
            client.reqMktData(
                self.REQUEST_ID,
                contract,
                "",
                True,
                False,
                [],
            )
            if not client.quote_ready.wait(self.timeout_seconds):
                detail = " | ".join(client.errors) or "no live bid/ask received"
                raise IbkrQuoteProviderError(
                    "Execution quote unavailable: " + detail
                )
            if (
                client.bid is None
                or client.ask is None
                or client.received_at is None
            ):
                raise IbkrQuoteProviderError(
                    "TWS signalled a quote without complete bid/ask values."
                )
            return ExecutionQuote(
                symbol=symbol.strip().upper(),
                bid=client.bid,
                ask=client.ask,
                bid_size=client.bid_size,
                ask_size=client.ask_size,
                received_at=client.received_at,
            )
        finally:
            if client.isConnected():
                try:
                    client.cancelMktData(self.REQUEST_ID)
                except Exception:
                    pass
                client.disconnect()
            if network_thread is not None:
                network_thread.join(timeout=2.0)
