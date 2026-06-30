from services.analysis.analyzers.base_analyzer import BaseAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


class MarketRegimeAnalyzer(BaseAnalyzer):
    """
    Analyseert het huidige marktregime van een aandeel.

    De MarketRegimeAnalyzer bepaalt niet of een aandeel koopwaardig is.
    Deze analyzer geeft alleen context over het technische markttype:
    bullish, bearish, sideways of choppy.
    """

    def analyze(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 50

        latest_close = indicators.get("latest_close")
        sma20 = indicators.get("sma20")
        sma50 = indicators.get("sma50")
        ema20 = indicators.get("ema20")
        ema50 = indicators.get("ema50")
        adx14 = indicators.get("adx14")
        bollinger = indicators.get("bollinger")

        bullish_alignment = self._is_bullish_alignment(
            latest_close=latest_close,
            sma20=sma20,
            sma50=sma50,
            ema20=ema20,
            ema50=ema50,
        )

        bearish_alignment = self._is_bearish_alignment(
            latest_close=latest_close,
            sma20=sma20,
            sma50=sma50,
            ema20=ema20,
            ema50=ema50,
        )

        adx_value = self._extract_adx_value(adx14)
        bollinger_width = self._extract_bollinger_width(bollinger)

        if bullish_alignment and adx_value is not None and adx_value >= 25:
            result.add_note("Market regime: strong bullish trend")
            return 90

        if bullish_alignment:
            result.add_note("Market regime: bullish trend")
            return 75

        if bearish_alignment and adx_value is not None and adx_value >= 25:
            result.add_note("Market regime: strong bearish trend")
            return 15

        if bearish_alignment:
            result.add_note("Market regime: bearish trend")
            return 30

        if adx_value is not None and adx_value < 18:
            if bollinger_width is not None and bollinger_width < 0.08:
                result.add_note("Market regime: low-volatility sideways market")
                return 55

            result.add_note("Market regime: sideways market")
            return 50

        if bollinger_width is not None and bollinger_width > 0.18:
            result.add_note("Market regime: choppy high-volatility market")
            return 40

        result.add_note("Market regime: neutral")
        return score

    def _is_bullish_alignment(
        self,
        latest_close,
        sma20,
        sma50,
        ema20,
        ema50,
    ) -> bool:
        values = [latest_close, sma20, sma50, ema20, ema50]

        if any(value is None for value in values):
            return False

        return (
            latest_close > sma20
            and sma20 > sma50
            and ema20 > ema50
        )

    def _is_bearish_alignment(
        self,
        latest_close,
        sma20,
        sma50,
        ema20,
        ema50,
    ) -> bool:
        values = [latest_close, sma20, sma50, ema20, ema50]

        if any(value is None for value in values):
            return False

        return (
            latest_close < sma20
            and sma20 < sma50
            and ema20 < ema50
        )

    def _extract_adx_value(self, adx14):
        if adx14 is None:
            return None

        if isinstance(adx14, dict):
            return adx14.get("adx")

        return adx14

    def _extract_bollinger_width(self, bollinger):
        if bollinger is None:
            return None

        if isinstance(bollinger, dict):
            return bollinger.get("band_width")

        if hasattr(bollinger, "band_width"):
            return bollinger.band_width

        return None