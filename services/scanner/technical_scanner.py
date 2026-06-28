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

    Sprint 7.5:
    - TechnicalScanner gebruikt de nieuwe Analysis Layer.
    - Indicatorberekeningen worden niet meer lokaal uitgevoerd.
    - AnalysisEngine is de enige bron voor technische scores.
    - Historical data blijft afkomstig uit HistoricalDataProvider.
    """

    def __init__(
        self,
        historical_provider: HistoricalDataProvider | None = None,
        analysis_engine: AnalysisEngine | None = None,
        period: str = "6mo",
        interval: str = "1d",
        batch_size: int = 100,
    ):
        self.historical_provider = historical_provider or YahooHistoricalDataProvider()
        self.analysis_engine = analysis_engine or AnalysisEngine()
        self.period = period
        self.interval = interval
        self.batch_size = batch_size

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

        history = self.historical_provider.get_history(
            symbols=symbols,
            period=self.period,
            interval=self.interval,
        )

        if not history:
            return []

        results: list[TechnicalScanResult] = []

        for symbol, data in history.items():
            quote = quote_map.get(symbol)

            if quote is None:
                continue

            if data is None or data.empty:
                continue

            result = self._scan_symbol_data(
                quote=quote,
                data=data,
            )

            if result is not None:
                results.append(result)

        return results

    def _scan_symbol_data(
        self,
        quote: Quote,
        data: pd.DataFrame,
    ) -> TechnicalScanResult | None:
        if not self._has_enough_data(data):
            return None

        analysis = self.analysis_engine.analyze(
            symbol=quote.symbol,
            candles=data,
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

    def _chunks(self, items: list[Quote], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]