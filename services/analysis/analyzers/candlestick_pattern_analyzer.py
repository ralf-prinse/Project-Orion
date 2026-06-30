import pandas as pd

from services.analysis.models import AnalysisResult, IndicatorResult


class CandlestickPatternAnalyzer:
    """
    Analyseert candlestick price-action patronen.

    Deze analyzer gebruikt bewust raw candledata in plaats van uitsluitend
    IndicatorResult, omdat candlestickpatronen price-action patronen zijn
    en geen klassieke technische indicatoren.

    Sprint 8.1 ondersteunt de eerste deterministische patronen:

    Bullish:
    - Hammer
    - Bullish Engulfing
    - Piercing Line

    Bearish:
    - Shooting Star
    - Bearish Engulfing
    - Dark Cloud Cover
    """

    def analyze(
        self,
        indicators: IndicatorResult,
        candles: pd.DataFrame,
        result: AnalysisResult,
    ) -> int:
        if candles is None or candles.empty or len(candles) < 2:
            result.add_note("Candlestick: insufficient candle data")
            return 50

        normalized_candles = self._normalize_candles(candles)

        if normalized_candles is None or normalized_candles.empty:
            result.add_note("Candlestick: invalid candle data")
            return 50

        latest = normalized_candles.iloc[-1]
        previous = normalized_candles.iloc[-2]

        bullish_patterns = []
        bearish_patterns = []

        if self._is_hammer(latest):
            bullish_patterns.append("hammer")

        if self._is_bullish_engulfing(previous, latest):
            bullish_patterns.append("bullish engulfing")

        if self._is_piercing_line(previous, latest):
            bullish_patterns.append("piercing line")

        if self._is_shooting_star(latest):
            bearish_patterns.append("shooting star")

        if self._is_bearish_engulfing(previous, latest):
            bearish_patterns.append("bearish engulfing")

        if self._is_dark_cloud_cover(previous, latest):
            bearish_patterns.append("dark cloud cover")

        score = self._calculate_score(
            bullish_patterns=bullish_patterns,
            bearish_patterns=bearish_patterns,
        )

        self._add_note(
            result=result,
            bullish_patterns=bullish_patterns,
            bearish_patterns=bearish_patterns,
            score=score,
        )

        return score

    def _normalize_candles(
        self,
        candles: pd.DataFrame,
    ) -> pd.DataFrame | None:
        required_columns = ["Open", "High", "Low", "Close"]

        if isinstance(candles.columns, pd.MultiIndex):
            normalized = {}

            for column_name in required_columns:
                if column_name in candles.columns.get_level_values(-1):
                    data = candles.xs(column_name, axis=1, level=-1)
                elif column_name in candles.columns.get_level_values(0):
                    data = candles[column_name]
                else:
                    return None

                if isinstance(data, pd.DataFrame):
                    if data.empty:
                        return None
                    normalized[column_name] = data.iloc[:, 0]
                else:
                    normalized[column_name] = data

            return pd.DataFrame(normalized).dropna()

        for column_name in required_columns:
            if column_name not in candles.columns:
                return None

        return candles[required_columns].dropna()

    def _is_bullish_candle(self, candle) -> bool:
        return float(candle["Close"]) > float(candle["Open"])

    def _is_bearish_candle(self, candle) -> bool:
        return float(candle["Close"]) < float(candle["Open"])

    def _body_size(self, candle) -> float:
        return abs(float(candle["Close"]) - float(candle["Open"]))

    def _upper_shadow(self, candle) -> float:
        return float(candle["High"]) - max(
            float(candle["Open"]),
            float(candle["Close"]),
        )

    def _lower_shadow(self, candle) -> float:
        return min(
            float(candle["Open"]),
            float(candle["Close"]),
        ) - float(candle["Low"])

    def _range_size(self, candle) -> float:
        return float(candle["High"]) - float(candle["Low"])

    def _midpoint(self, candle) -> float:
        return (float(candle["Open"]) + float(candle["Close"])) / 2

    def _is_hammer(self, candle) -> bool:
        body = self._body_size(candle)
        lower_shadow = self._lower_shadow(candle)
        upper_shadow = self._upper_shadow(candle)
        candle_range = self._range_size(candle)

        if candle_range <= 0 or body <= 0:
            return False

        return (
            lower_shadow >= body * 2
            and upper_shadow <= body
            and body / candle_range <= 0.40
        )

    def _is_shooting_star(self, candle) -> bool:
        body = self._body_size(candle)
        lower_shadow = self._lower_shadow(candle)
        upper_shadow = self._upper_shadow(candle)
        candle_range = self._range_size(candle)

        if candle_range <= 0 or body <= 0:
            return False

        return (
            upper_shadow >= body * 2
            and lower_shadow <= body
            and body / candle_range <= 0.40
        )

    def _is_bullish_engulfing(self, previous, latest) -> bool:
        if not self._is_bearish_candle(previous):
            return False

        if not self._is_bullish_candle(latest):
            return False

        previous_open = float(previous["Open"])
        previous_close = float(previous["Close"])
        latest_open = float(latest["Open"])
        latest_close = float(latest["Close"])

        return latest_open <= previous_close and latest_close >= previous_open

    def _is_bearish_engulfing(self, previous, latest) -> bool:
        if not self._is_bullish_candle(previous):
            return False

        if not self._is_bearish_candle(latest):
            return False

        previous_open = float(previous["Open"])
        previous_close = float(previous["Close"])
        latest_open = float(latest["Open"])
        latest_close = float(latest["Close"])

        return latest_open >= previous_close and latest_close <= previous_open

    def _is_piercing_line(self, previous, latest) -> bool:
        if not self._is_bearish_candle(previous):
            return False

        if not self._is_bullish_candle(latest):
            return False

        previous_close = float(previous["Close"])
        latest_open = float(latest["Open"])
        latest_close = float(latest["Close"])

        return (
            latest_open < previous_close
            and latest_close > self._midpoint(previous)
            and latest_close < float(previous["Open"])
        )

    def _is_dark_cloud_cover(self, previous, latest) -> bool:
        if not self._is_bullish_candle(previous):
            return False

        if not self._is_bearish_candle(latest):
            return False

        previous_close = float(previous["Close"])
        latest_open = float(latest["Open"])
        latest_close = float(latest["Close"])

        return (
            latest_open > previous_close
            and latest_close < self._midpoint(previous)
            and latest_close > float(previous["Open"])
        )

    def _calculate_score(
        self,
        bullish_patterns: list[str],
        bearish_patterns: list[str],
    ) -> int:
        bullish_score = len(bullish_patterns) * 20
        bearish_score = len(bearish_patterns) * 20

        score = 50 + bullish_score - bearish_score

        return max(0, min(100, score))

    def _add_note(
        self,
        result: AnalysisResult,
        bullish_patterns: list[str],
        bearish_patterns: list[str],
        score: int,
    ) -> None:
        if bullish_patterns:
            patterns = ", ".join(bullish_patterns)
            result.add_note(f"Candlestick: bullish pattern detected ({patterns})")

        if bearish_patterns:
            patterns = ", ".join(bearish_patterns)
            result.add_note(f"Candlestick: bearish pattern detected ({patterns})")

        if not bullish_patterns and not bearish_patterns:
            result.add_note("Candlestick: no major pattern detected")
            return

        result.add_note(f"Candlestick score: {score}")