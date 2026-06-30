from dataclasses import dataclass

import pandas as pd

from services.analysis.analysis_engine import AnalysisEngine
from services.analysis.models import AnalysisResult
from services.market_data.historical_provider import HistoricalDataProvider
from services.market_data.yahoo_historical_provider import YahooHistoricalDataProvider
from services.scanner.quote_service import Quote


@dataclass
class TechnicalScanResult:
    symbol: str
    quote: Quote
    technical_score: float
    signal: str
    reason: str
    analysis: AnalysisResult | None = None


class TechnicalScanner:
    """
    Voert technische analyse uit op de beste scanner-kandidaten.

    Sprint 8.0:
    - TechnicalScanner gebruikt de modulaire Analysis Layer.
    - Historical data blijft afkomstig uit HistoricalDataProvider.
    - SPY wordt gebruikt als standaard benchmark voor relative strength.
    - Benchmark-historie wordt één keer per batch opgehaald.
    """

    def __init__(
        self,
        historical_provider: HistoricalDataProvider | None = None,
        analysis_engine: AnalysisEngine | None = None,
        period: str = "6mo",
        interval: str = "1d",
        batch_size: int = 100,
        benchmark_symbol: str = "SPY",
    ):
        self.historical_provider = historical_provider or YahooHistoricalDataProvider()
        self.analysis_engine = analysis_engine or AnalysisEngine()
        self.period = period
        self.interval = interval
        self.batch_size = batch_size
        self.benchmark_symbol = benchmark_symbol

    def scan(self, quotes: list[Quote]) -> list[TechnicalScanResult]:
        if not quotes:
            return []

        results: list[TechnicalScanResult] = []

        for quote_batch in self._chunks(quotes, self.batch_size):
            batch_results = self._scan_batch(quote_batch)
            results.extend(batch_results)

        return results

    def _scan_batch(self, quotes: list[Quote]) -> list[TechnicalScanResult]:
        if not quotes:
            return []

        symbols = [quote.symbol for quote in quotes]
        quote_map = {quote.symbol: quote for quote in quotes}

        symbols_with_benchmark = self._add_benchmark_symbol(symbols)

        history = self.historical_provider.get_history(
            symbols=symbols_with_benchmark,
            period=self.period,
            interval=self.interval,
        )

        if not history:
            return []

        benchmark_candles = history.get(self.benchmark_symbol)

        results: list[TechnicalScanResult] = []

        for symbol, data in history.items():
            if symbol == self.benchmark_symbol:
                continue

            quote = quote_map.get(symbol)

            if quote is None:
                continue

            if data is None or data.empty:
                continue

            result = self._scan_symbol_data(
                quote=quote,
                data=data,
                benchmark_candles=benchmark_candles,
            )

            if result is not None:
                results.append(result)

        return results

    def _scan_symbol_data(
        self,
        quote: Quote,
        data: pd.DataFrame,
        benchmark_candles: pd.DataFrame | None = None,
    ) -> TechnicalScanResult | None:
        if not self._has_enough_data(data):
            return None

        analysis = self.analysis_engine.analyze(
            symbol=quote.symbol,
            candles=data,
            benchmark_candles=benchmark_candles,
        )

        technical_score = float(analysis.overall_score)
        signal = self._determine_signal(technical_score)
        reason = self._build_reason(analysis)

        return TechnicalScanResult(
            symbol=quote.symbol,
            quote=quote,
            technical_score=technical_score,
            signal=signal,
            reason=reason,
            analysis=analysis,
        )

    def _determine_signal(self, technical_score: float) -> str:
        if technical_score >= 80:
            return "BUY"

        if technical_score >= 50:
            return "HOLD"

        return "IGNORE"

    def _build_reason(self, analysis: AnalysisResult) -> str:
        if not analysis.notes:
            return "Geen sterke technische setup"

        return ", ".join(analysis.notes)

    def _has_enough_data(self, data: pd.DataFrame) -> bool:
        if data is None or data.empty:
            return False

        return len(data) >= 60

    def _add_benchmark_symbol(self, symbols: list[str]) -> list[str]:
        if self.benchmark_symbol in symbols:
            return symbols

        return symbols + [self.benchmark_symbol]

    def _chunks(self, items: list[Quote], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]