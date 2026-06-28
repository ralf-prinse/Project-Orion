from services.analysis.models import AnalysisResult, IndicatorResult


class VolatilityAnalyzer:
    """
    Analyseert volatiliteit op basis van berekende indicatoren.

    Verantwoordelijkheid:
    - Alleen volatilityscore bepalen.
    - Alleen volatilitygerelateerde analysis notes toevoegen.
    - Geen indicatoren berekenen.
    - Geen BUY/HOLD/IGNORE beslissingen nemen.
    """

    def analyze(
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