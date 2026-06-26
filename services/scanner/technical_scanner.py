from dataclasses import dataclass

import pandas as pd

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


class TechnicalScanner:
    """
    Voert technische analyse uit op de beste kandidaten.

    Vanaf Sprint 6.6:
    - TechnicalScanner downloadt zelf geen historische data meer.
    - Alle historische candles komen via HistoricalDataProvider.
    - yfinance mag hier niet meer rechtstreeks gebruikt worden.
    """

    def __init__(
        self,
        historical_provider: HistoricalDataProvider | None = None,
        period: str = "6mo",
        interval: str = "1d",
        batch_size: int = 100,
    ):
        self.historical_provider = historical_provider or YahooHistoricalDataProvider()
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
        close = self._extract_close_series(data)

        if close is None:
            return None

        close = close.dropna()

        if len(close) < 60:
            return None

        sma20 = close.rolling(window=20).mean()
        sma50 = close.rolling(window=50).mean()
        rsi14 = self._calculate_rsi(close, period=14)

        latest_close = float(close.iloc[-1])
        latest_sma20 = float(sma20.iloc[-1])
        latest_sma50 = float(sma50.iloc[-1])
        latest_rsi = float(rsi14.iloc[-1])

        close_20_days_ago = float(close.iloc[-20])

        if close_20_days_ago <= 0:
            return None

        latest_momentum = ((latest_close - close_20_days_ago) / close_20_days_ago) * 100

        score = 0.0
        reasons: list[str] = []

        if latest_close > latest_sma20:
            score += 20
            reasons.append("Koers boven SMA20")

        if latest_close > latest_sma50:
            score += 20
            reasons.append("Koers boven SMA50")

        if latest_sma20 > latest_sma50:
            score += 20
            reasons.append("Korte trend sterker dan lange trend")

        if 45 <= latest_rsi <= 70:
            score += 20
            reasons.append("RSI gezond voor swing trade")

        if latest_momentum > 3:
            score += 20
            reasons.append("Positief 20-daags momentum")

        if score >= 80:
            signal = "BUY"
        elif score >= 50:
            signal = "HOLD"
        else:
            signal = "IGNORE"

        reason = ", ".join(reasons) if reasons else "Geen sterke technische setup"

        return TechnicalScanResult(
            symbol=quote.symbol,
            quote=quote,
            technical_score=score,
            signal=signal,
            reason=reason,
        )

    def _extract_close_series(self, data: pd.DataFrame) -> pd.Series | None:
        if isinstance(data.columns, pd.MultiIndex):
            if "Close" in data.columns.get_level_values(-1):
                close_data = data.xs("Close", axis=1, level=-1)
            elif "Close" in data.columns.get_level_values(0):
                close_data = data["Close"]
            else:
                return None

            if isinstance(close_data, pd.DataFrame):
                if close_data.empty:
                    return None

                return close_data.iloc[:, 0]

            return close_data

        if "Close" not in data.columns:
            return None

        close_data = data["Close"]

        if isinstance(close_data, pd.DataFrame):
            if close_data.empty:
                return None

            return close_data.iloc[:, 0]

        return close_data

    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        average_gain = gain.rolling(window=period).mean()
        average_loss = loss.rolling(window=period).mean()

        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def _chunks(self, items: list[Quote], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]