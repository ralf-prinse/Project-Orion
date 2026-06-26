from services.analysis.indicator_engine import IndicatorEngine
from services.analysis.models import AnalysisResult, IndicatorResult


class AnalysisEngine:
    """
    Centrale technische analyse-engine van Project Orion.

    Sprint 7.4:
    - Roept IndicatorEngine aan.
    - Zet indicatorwaarden om naar technische scores.
    - Berekent trend, momentum, volatility en overall score.
    """

    def __init__(self, indicator_engine: IndicatorEngine | None = None):
        self.indicator_engine = indicator_engine or IndicatorEngine()

    def analyze(self, symbol: str, candles) -> AnalysisResult:
        indicators = self.indicator_engine.calculate(
            symbol=symbol,
            candles=candles,
        )

        return self._build_analysis_result(
            symbol=symbol,
            indicators=indicators,
        )

    def _build_analysis_result(
        self,
        symbol: str,
        indicators: IndicatorResult,
    ) -> AnalysisResult:
        result = AnalysisResult(symbol=symbol)

        if indicators.has("error"):
            result.add_note(indicators.get("error"))
            return result

        result.trend_score = self._calculate_trend_score(
            indicators=indicators,
            result=result,
        )

        result.momentum_score = self._calculate_momentum_score(
            indicators=indicators,
            result=result,
        )

        result.volatility_score = self._calculate_volatility_score(
            indicators=indicators,
            result=result,
        )

        result.overall_score = self._calculate_overall_score(result)

        result.add_note(f"Overall technical score: {result.overall_score}")

        return result

    def _calculate_trend_score(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 0

        sma20 = indicators.get("sma20")
        sma50 = indicators.get("sma50")
        ema20 = indicators.get("ema20")
        ema50 = indicators.get("ema50")
        adx = indicators.get("adx14")

        if sma20 is not None and sma50 is not None:
            if sma20 > sma50:
                score += 30
                result.add_note("Trend: SMA20 boven SMA50")
            else:
                result.add_note("Trend: SMA20 niet boven SMA50")

        if ema20 is not None and ema50 is not None:
            if ema20 > ema50:
                score += 30
                result.add_note("Trend: EMA20 boven EMA50")
            else:
                result.add_note("Trend: EMA20 niet boven EMA50")

        if isinstance(adx, dict):
            adx_value = adx.get("adx")
            plus_di = adx.get("plus_di")
            minus_di = adx.get("minus_di")

            if adx_value is not None and adx_value >= 25:
                score += 20
                result.add_note("Trend: ADX bevestigt voldoende trendsterkte")

            if (
                plus_di is not None
                and minus_di is not None
                and plus_di > minus_di
            ):
                score += 20
                result.add_note("Trend: +DI boven -DI")

        return min(score, 100)

    def _calculate_momentum_score(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 0

        rsi = indicators.get("rsi14")
        macd = indicators.get("macd")

        if rsi is not None:
            if 45 <= rsi <= 70:
                score += 40
                result.add_note("Momentum: RSI gezond voor swing trade")
            elif 35 <= rsi < 45:
                score += 20
                result.add_note("Momentum: RSI zwak maar niet extreem")
            elif rsi > 70:
                score += 10
                result.add_note("Momentum: RSI mogelijk overbought")
            else:
                result.add_note("Momentum: RSI ongunstig")

        if isinstance(macd, dict):
            macd_line = macd.get("macd")
            signal_line = macd.get("signal")
            histogram = macd.get("histogram")

            if (
                macd_line is not None
                and signal_line is not None
                and macd_line > signal_line
            ):
                score += 35
                result.add_note("Momentum: MACD boven signaallijn")
            else:
                result.add_note("Momentum: MACD onder signaallijn")

            if histogram is not None and histogram > 0:
                score += 25
                result.add_note("Momentum: MACD histogram positief")

        return min(score, 100)

    def _calculate_volatility_score(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 0

        atr = indicators.get("atr14")
        bollinger = indicators.get("bollinger")

        if atr is not None and atr > 0:
            score += 40
            result.add_note("Volatility: ATR beschikbaar en geldig")

        if isinstance(bollinger, dict):
            width = bollinger.get("width")

            if width is not None:
                if 5 <= width <= 20:
                    score += 60
                    result.add_note("Volatility: Bollinger width gezond")
                elif width < 5:
                    score += 30
                    result.add_note("Volatility: Bollinger width laag")
                else:
                    score += 20
                    result.add_note("Volatility: Bollinger width hoog")

        return min(score, 100)

    def _calculate_overall_score(
        self,
        result: AnalysisResult,
    ) -> int:
        weighted_score = (
            result.trend_score * 0.40
            + result.momentum_score * 0.35
            + result.volatility_score * 0.25
        )

        return int(round(weighted_score))