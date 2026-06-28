from services.analysis.models import AnalysisResult, IndicatorResult


class TrendAnalyzer:
    """
    Analyseert trendkwaliteit op basis van berekende indicatoren.

    Verantwoordelijkheid:
    - Alleen trendscore bepalen.
    - Alleen trendgerelateerde analysis notes toevoegen.
    - Geen indicatoren berekenen.
    - Geen BUY/HOLD/IGNORE beslissingen nemen.
    """

    def analyze(
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