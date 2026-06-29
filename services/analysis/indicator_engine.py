import pandas as pd

from services.analysis.indicator_library.advanced_momentum import calculate_macd
from services.analysis.indicator_library.momentum import calculate_rsi
from services.analysis.indicator_library.moving_averages import (
    calculate_ema,
    calculate_sma,
)
from services.analysis.indicator_library.trend_strength import calculate_adx
from services.analysis.indicator_library.volatility import (
    calculate_atr,
    calculate_bollinger_bands,
)
from services.analysis.models import IndicatorResult


class IndicatorEngine:
    """
    Centrale manager voor alle technische indicatoren.

    Sprint 7.7:
    - Berekent technische indicatoren.
    - Berekent basisstructuurwaarden voor StructureAnalyzer.
    """

    def calculate(
        self,
        symbol: str,
        candles: pd.DataFrame,
    ) -> IndicatorResult:
        result = IndicatorResult(symbol=symbol)

        close = self._extract_close_series(candles)
        high = self._extract_price_series(candles, "High")
        low = self._extract_price_series(candles, "Low")

        if close is None:
            result.set("error", "Geen geldige Close-kolom gevonden")
            return result

        result.set("sma20", calculate_sma(close, period=20))
        result.set("sma50", calculate_sma(close, period=50))

        result.set("ema20", calculate_ema(close, period=20))
        result.set("ema50", calculate_ema(close, period=50))

        result.set("rsi14", calculate_rsi(close, period=14))

        result.set("macd", calculate_macd(close))
        result.set("atr14", calculate_atr(candles, period=14))
        result.set("bollinger", calculate_bollinger_bands(close))
        result.set("adx14", calculate_adx(candles, period=14))

        self._add_structure_values(
            result=result,
            close=close,
            high=high,
            low=low,
        )

        return result

    def _add_structure_values(
        self,
        result: IndicatorResult,
        close: pd.Series,
        high: pd.Series | None,
        low: pd.Series | None,
    ) -> None:
        if close is None or close.empty:
            return

        result.set("latest_close", float(close.dropna().iloc[-1]))

        if high is None or low is None:
            return

        high = high.dropna()
        low = low.dropna()

        if len(high) < 40 or len(low) < 40:
            return

        recent_high_20 = float(high.iloc[-20:].max())
        recent_low_20 = float(low.iloc[-20:].min())

        previous_high_20 = float(high.iloc[-40:-20].max())
        previous_low_20 = float(low.iloc[-40:-20].min())

        result.set("recent_high_20", recent_high_20)
        result.set("recent_low_20", recent_low_20)
        result.set("previous_high_20", previous_high_20)
        result.set("previous_low_20", previous_low_20)

    def _extract_close_series(
        self,
        candles: pd.DataFrame,
    ) -> pd.Series | None:
        return self._extract_price_series(candles, "Close")

    def _extract_price_series(
        self,
        candles: pd.DataFrame,
        column_name: str,
    ) -> pd.Series | None:
        if candles is None or candles.empty:
            return None

        if isinstance(candles.columns, pd.MultiIndex):
            if column_name in candles.columns.get_level_values(-1):
                price_data = candles.xs(column_name, axis=1, level=-1)
            elif column_name in candles.columns.get_level_values(0):
                price_data = candles[column_name]
            else:
                return None

            if isinstance(price_data, pd.DataFrame):
                if price_data.empty:
                    return None

                return price_data.iloc[:, 0]

            return price_data

        if column_name not in candles.columns:
            return None

        price_data = candles[column_name]

        if isinstance(price_data, pd.DataFrame):
            if price_data.empty:
                return None

            return price_data.iloc[:, 0]

        return price_data