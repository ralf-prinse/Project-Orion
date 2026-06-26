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

    Sprint 7.3:
    - Berekent SMA20 en SMA50.
    - Berekent EMA20 en EMA50.
    - Berekent RSI14.
    - Berekent MACD.
    - Berekent ATR14.
    - Berekent Bollinger Bands.
    - Berekent ADX14.
    """

    def calculate(
        self,
        symbol: str,
        candles: pd.DataFrame,
    ) -> IndicatorResult:
        result = IndicatorResult(symbol=symbol)

        close = self._extract_close_series(candles)

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

        return result

    def _extract_close_series(
        self,
        candles: pd.DataFrame,
    ) -> pd.Series | None:
        if candles is None or candles.empty:
            return None

        if isinstance(candles.columns, pd.MultiIndex):
            if "Close" in candles.columns.get_level_values(-1):
                close_data = candles.xs("Close", axis=1, level=-1)
            elif "Close" in candles.columns.get_level_values(0):
                close_data = candles["Close"]
            else:
                return None

            if isinstance(close_data, pd.DataFrame):
                if close_data.empty:
                    return None

                return close_data.iloc[:, 0]

            return close_data

        if "Close" not in candles.columns:
            return None

        close_data = candles["Close"]

        if isinstance(close_data, pd.DataFrame):
            if close_data.empty:
                return None

            return close_data.iloc[:, 0]

        return close_data