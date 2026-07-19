from __future__ import annotations

from datetime import UTC, datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner
from services.market_session_service import MarketSessionService


class OneSymbolWatchlist:
    def load_symbols(self) -> list[str]:
        return ["AAPL"]


class ProviderMustNotRun:
    def get_historical_data(self, **kwargs):
        raise AssertionError("Closed-market symbols must not fetch data.")


def test_scanner_skips_buy_analysis_when_symbol_market_is_closed() -> None:
    saturday = datetime(2026, 7, 18, 14, 0, tzinfo=UTC)
    scanner = LivePaperMarketScanner(
        config=LivePaperTradingConfig(max_symbols=1),
        provider=ProviderMustNotRun(),
        watchlist_service=OneSymbolWatchlist(),
        market_session_service=MarketSessionService(),
        clock=lambda: saturday,
    )

    result = scanner.run()

    assert result.scanned_symbols == 1
    assert result.succeeded_symbols == 0
    assert result.failed_symbols == 1
    assert result.candidates == []
    assert "Market XUSA is closed" in result.failed_symbol_errors["AAPL"]
