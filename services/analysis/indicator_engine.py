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

    Sprint 8.0:
    - Berekent technische indicatoren.
    - Berekent basisstructuurwaarden voor StructureAnalyzer.
    - Berekent volumegegevens voor VolumeAnalyzer.
    - Ondersteunt optionele benchmark candles voor RelativeStrengthAnalyzer.
    """

    def calculate(
        self,
        symbol: str,
        candles: pd.DataFrame,
        benchmark_candles: pd.DataFrame | None = None,
    ) -> IndicatorResult:
        result = IndicatorResult(symbol=symbol)

        close = self._extract_close_series(candles)
        high = self._extract_price_series(candles, "High")
        low = self._extract_price_series(candles, "Low")
        volume = self._extract_price_series(candles, "Volume")

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

        self._add_volume_values(
            result=result,
            volume=volume,
        )

        self._add_relative_strength_values(
            result=result,
            close=close,
            benchmark_candles=benchmark_candles,
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

        close = close.dropna()

        if close.empty:
            return

        result.set("latest_close", float(close.iloc[-1]))

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

    def _add_volume_values(
        self,
        result: IndicatorResult,
        volume: pd.Series | None,
    ) -> None:
        if volume is None:
            return

        volume = volume.dropna()

        if len(volume) < 20:
            return

        latest_volume = float(volume.iloc[-1])
        average_volume_20 = float(volume.iloc[-20:].mean())

        result.set("latest_volume", latest_volume)
        result.set("average_volume_20", average_volume_20)

        if average_volume_20 > 0:
            relative_volume = latest_volume / average_volume_20
            result.set("relative_volume_20", float(relative_volume))

        if len(volume) >= 40:
            previous_average_volume_20 = float(volume.iloc[-40:-20].mean())
            result.set("previous_average_volume_20", previous_average_volume_20)

            if previous_average_volume_20 > 0:
                volume_trend_20 = (
                    (average_volume_20 - previous_average_volume_20)
                    / previous_average_volume_20
                ) * 100

                result.set("volume_trend_20", float(volume_trend_20))

    def _add_relative_strength_values(
        self,
        result: IndicatorResult,
        close: pd.Series,
        benchmark_candles: pd.DataFrame | None,
    ) -> None:
        if benchmark_candles is None:
            return

        benchmark_close = self._extract_close_series(benchmark_candles)

        if benchmark_close is None:
            return

        close = close.dropna()
        benchmark_close = benchmark_close.dropna()

        if close.empty or benchmark_close.empty:
            return

        relative_strength_20 = self._calculate_relative_strength(
            close=close,
            benchmark_close=benchmark_close,
            period=20,
        )

        relative_strength_50 = self._calculate_relative_strength(
            close=close,
            benchmark_close=benchmark_close,
            period=50,
        )

        if relative_strength_20 is not None:
            result.set("relative_strength_20", relative_strength_20)

        if relative_strength_50 is not None:
            result.set("relative_strength_50", relative_strength_50)

        if relative_strength_20 is not None and relative_strength_50 is not None:
            relative_strength_trend = relative_strength_20 - relative_strength_50
            result.set("relative_strength_trend", float(relative_strength_trend))

    def _calculate_relative_strength(
        self,
        close: pd.Series,
        benchmark_close: pd.Series,
        period: int,
    ) -> float | None:
        if len(close) < period + 1 or len(benchmark_close) < period + 1:
            return None

        stock_start = float(close.iloc[-period - 1])
        stock_end = float(close.iloc[-1])

        benchmark_start = float(benchmark_close.iloc[-period - 1])
        benchmark_end = float(benchmark_close.iloc[-1])

        if stock_start <= 0 or benchmark_start <= 0:
            return None

        stock_return = ((stock_end - stock_start) / stock_start) * 100
        benchmark_return = (
            (benchmark_end - benchmark_start) / benchmark_start
        ) * 100

        return float(stock_return - benchmark_return)

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