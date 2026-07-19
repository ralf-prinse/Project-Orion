from __future__ import annotations

import threading
from datetime import UTC, datetime

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from models.news_event import RawNewsItem
from services.ibkr.ibkr_stock_contract_factory import (
    IbkrStockContractFactory,
)


class IbkrNewsProviderError(RuntimeError):
    pass


class _IbkrNewsClient(EWrapper, EClient):
    INFORMATIONAL_ERROR_CODES = {2104, 2106, 2107, 2108, 2158}

    def __init__(self) -> None:
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.connection_ready = threading.Event()
        self.providers_ready = threading.Event()
        self.providers = []
        self.contract_events: dict[int, threading.Event] = {}
        self.contract_ids: dict[int, list[int]] = {}
        self.news_events: dict[int, threading.Event] = {}
        self.news_items: dict[int, list[tuple]] = {}
        self.errors: list[tuple[int, int, str]] = []

    def nextValidId(self, orderId: int) -> None:
        self.connection_ready.set()

    def newsProviders(self, newsProviders) -> None:
        self.providers = list(newsProviders or [])
        self.providers_ready.set()

    def contractDetails(self, reqId, contractDetails) -> None:
        contract = getattr(contractDetails, "contract", None)
        con_id = int(getattr(contract, "conId", 0) or 0)
        if con_id > 0:
            self.contract_ids.setdefault(int(reqId), []).append(con_id)

    def contractDetailsEnd(self, reqId: int) -> None:
        event = self.contract_events.get(int(reqId))
        if event is not None:
            event.set()

    def historicalNews(
        self,
        requestId,
        time,
        providerCode,
        articleId,
        headline,
    ) -> None:
        self.news_items.setdefault(int(requestId), []).append(
            (time, providerCode, articleId, headline)
        )

    def historicalNewsEnd(self, requestId, hasMore) -> None:
        event = self.news_events.get(int(requestId))
        if event is not None:
            event.set()

    def error(
        self,
        reqId,
        errorCode,
        errorString,
        advancedOrderRejectJson="",
    ) -> None:
        code = int(errorCode)
        if code in self.INFORMATIONAL_ERROR_CODES:
            return
        self.errors.append((int(reqId), code, str(errorString)))


class IbkrNewsProvider:
    """Read-only historical headline provider for TWS Paper."""

    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 7497,
        client_id: int = 130,
        timeout_seconds: float = 10.0,
        provider_codes: tuple[str, ...] = (),
        client: _IbkrNewsClient | None = None,
        contract_factory: IbkrStockContractFactory | None = None,
    ) -> None:
        if port <= 0:
            raise ValueError("port must be greater than zero.")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero.")
        self.host = host.strip()
        self.port = int(port)
        self.client_id = int(client_id)
        self.timeout_seconds = float(timeout_seconds)
        self.provider_codes = tuple(
            code.strip().upper()
            for code in provider_codes
            if code.strip()
        )
        self.client = client or _IbkrNewsClient()
        self.contract_factory = (
            contract_factory or IbkrStockContractFactory()
        )
        self._network_thread: threading.Thread | None = None
        self._request_id = 20_000

    @property
    def name(self) -> str:
        return "IBKR"

    def fetch_recent(
        self,
        *,
        symbols: tuple[str, ...],
        since: datetime,
        max_articles_per_symbol: int,
    ) -> tuple[RawNewsItem, ...]:
        if max_articles_per_symbol < 1:
            raise ValueError("max_articles_per_symbol must be at least 1.")
        if not symbols:
            return ()

        self._connect()
        try:
            provider_codes = self._resolve_provider_codes()
            items: list[RawNewsItem] = []
            for symbol in symbols:
                con_id = self._resolve_contract_id(symbol)
                request_id = self._next_request_id()
                event = threading.Event()
                self.client.news_events[request_id] = event
                self.client.news_items[request_id] = []
                self.client.errors = []
                self.client.reqHistoricalNews(
                    request_id,
                    con_id,
                    "+".join(provider_codes),
                    self._as_utc(since).strftime("%Y-%m-%d %H:%M:%S.0"),
                    "",
                    int(max_articles_per_symbol),
                    [],
                )
                self._wait(event, f"historical news for {symbol}")
                self._raise_errors(f"requesting news for {symbol}")
                items.extend(
                    RawNewsItem(
                        provider=str(provider_code).strip().upper(),
                        article_id=str(article_id).strip(),
                        headline=str(headline).strip(),
                        published_at=self._parse_news_time(raw_time),
                        symbols=(symbol.strip().upper(),),
                    )
                    for raw_time, provider_code, article_id, headline
                    in self.client.news_items.get(request_id, [])
                )
            return tuple(items)
        finally:
            self._disconnect()

    def _connect(self) -> None:
        if self.client.isConnected():
            return
        self.client.connection_ready.clear()
        self.client.providers_ready.clear()
        self.client.errors = []
        self.client.connect(self.host, self.port, clientId=self.client_id)
        self._network_thread = threading.Thread(
            target=self.client.run,
            name="ibkr-news-provider",
            daemon=True,
        )
        self._network_thread.start()
        self._wait(self.client.connection_ready, "TWS news connection")
        self._raise_errors("connecting to TWS news")

    def _resolve_provider_codes(self) -> tuple[str, ...]:
        if self.provider_codes:
            return self.provider_codes
        self.client.providers_ready.clear()
        self.client.errors = []
        self.client.reqNewsProviders()
        self._wait(self.client.providers_ready, "news provider list")
        self._raise_errors("reading news providers")
        codes = tuple(
            dict.fromkeys(
                str(getattr(provider, "code", "")).strip().upper()
                for provider in self.client.providers
                if str(getattr(provider, "code", "")).strip()
            )
        )
        if not codes:
            raise IbkrNewsProviderError(
                "TWS returned no API-enabled news providers."
            )
        return codes

    def _resolve_contract_id(self, symbol: str) -> int:
        request_id = self._next_request_id()
        event = threading.Event()
        self.client.contract_events[request_id] = event
        self.client.contract_ids[request_id] = []
        self.client.errors = []
        self.client.reqContractDetails(
            request_id,
            self.contract_factory.build(symbol),
        )
        self._wait(event, f"contract details for {symbol}")
        self._raise_errors(f"resolving contract for {symbol}")
        contract_ids = self.client.contract_ids.get(request_id, [])
        if not contract_ids:
            raise IbkrNewsProviderError(
                f"IBKR returned no contract for {symbol}."
            )
        return contract_ids[0]

    def _disconnect(self) -> None:
        if self.client.isConnected():
            self.client.disconnect()
        if self._network_thread is not None:
            self._network_thread.join(timeout=2.0)
            self._network_thread = None

    def _wait(self, event: threading.Event, description: str) -> None:
        if not event.wait(self.timeout_seconds):
            raise IbkrNewsProviderError(
                f"Timeout while waiting for {description}."
            )

    def _raise_errors(self, operation: str) -> None:
        if not self.client.errors:
            return
        messages = " | ".join(
            f"reqId={req_id}, code={code}, message={message}"
            for req_id, code, message in self.client.errors
        )
        raise IbkrNewsProviderError(
            f"IBKR API error while {operation}: {messages}"
        )

    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _parse_news_time(self, value) -> datetime:
        raw = str(value).strip()
        try:
            epoch = int(raw)
            if abs(epoch) >= 100_000_000_000:
                epoch /= 1000
            return datetime.fromtimestamp(epoch, tz=UTC)
        except (TypeError, ValueError, OSError):
            pass
        for pattern in (
            "%Y-%m-%d %H:%M:%S",
            "%Y%m%d %H:%M:%S.%f",
            "%Y%m%d %H:%M:%S",
        ):
            try:
                return datetime.strptime(raw, pattern).replace(tzinfo=UTC)
            except ValueError:
                continue
        raise IbkrNewsProviderError(
            f"IBKR returned an invalid news timestamp: {value!r}."
        )

    def _as_utc(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
