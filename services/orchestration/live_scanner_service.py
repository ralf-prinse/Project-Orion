from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from services.scanner.quote_service import Quote, QuoteService
from services.scanner.technical_scanner import TechnicalScanResult, TechnicalScanner
from services.watchlist_service import WatchlistService


@dataclass(frozen=True)
class LiveScannerSnapshot:
    """
    Deterministic snapshot of one live scanner cycle.

    This model contains scanner output only.
    It contains no UI logic and no AI decisions.
    """

    timestamp: datetime
    symbols: tuple[str, ...]
    quotes: tuple[Quote, ...]
    technical_results: tuple[TechnicalScanResult, ...]
    errors: tuple[str, ...] = field(default_factory=tuple)

    @property
    def total_symbols(self) -> int:
        return len(self.symbols)

    @property
    def total_quotes(self) -> int:
        return len(self.quotes)

    @property
    def total_results(self) -> int:
        return len(self.technical_results)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def top_results(self) -> tuple[TechnicalScanResult, ...]:
        return tuple(
            sorted(
                self.technical_results,
                key=lambda result: result.technical_score,
                reverse=True,
            )
        )


class LiveScannerService:
    """
    Near-live scanner orchestration service.

    Responsibilities:
    - load symbols from WatchlistService;
    - fetch quotes through QuoteService;
    - run TechnicalScanner;
    - store the latest deterministic scanner snapshot.

    This service does not calculate trading decisions.
    This service does not render UI.
    This service does not call AI.
    """

    def __init__(
        self,
        watchlist_service: WatchlistService | None = None,
        quote_service: QuoteService | None = None,
        technical_scanner: TechnicalScanner | None = None,
    ):
        self.watchlist_service = watchlist_service or WatchlistService()
        self.quote_service = quote_service or QuoteService()
        self.technical_scanner = technical_scanner or TechnicalScanner()

        self._running = False
        self._last_snapshot: LiveScannerSnapshot | None = None

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def last_snapshot(self) -> LiveScannerSnapshot | None:
        return self._last_snapshot

    def start(self) -> LiveScannerSnapshot:
        """
        Start the scanner and immediately execute one scan cycle.
        """

        self._running = True
        return self.scan_once()

    def stop(self) -> None:
        """
        Stop the scanner.

        Scheduling is owned by the caller.
        """

        self._running = False

    def scan_once(self) -> LiveScannerSnapshot:
        """
        Execute one deterministic scanner cycle.

        Provider errors are captured inside the snapshot so the UI can
        display scanner status without crashing the application.
        """

        errors: list[str] = []
        symbols: list[str] = []
        quotes: list[Quote] = []
        technical_results: list[TechnicalScanResult] = []

        try:
            symbols = self.watchlist_service.load_symbols()
        except Exception as error:
            errors.append(f"Watchlist error: {error}")

        if symbols:
            try:
                quotes = self.quote_service.get_quotes(symbols)
            except Exception as error:
                errors.append(f"Quote error: {error}")

        if quotes:
            try:
                technical_results = self.technical_scanner.scan(quotes)
            except Exception as error:
                errors.append(f"Technical scanner error: {error}")

        snapshot = LiveScannerSnapshot(
            timestamp=datetime.now(),
            symbols=tuple(symbols),
            quotes=tuple(quotes),
            technical_results=tuple(technical_results),
            errors=tuple(errors),
        )

        self._last_snapshot = snapshot

        return snapshot