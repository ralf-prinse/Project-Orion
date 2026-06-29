from services.analysis.analyzers.base_analyzer import BaseAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


class StructureAnalyzer(BaseAnalyzer):
    """
    Analyseert marktstructuur op basis van prijsniveaus.

    Verantwoordelijkheid:
    - Alleen structurescore bepalen.
    - Alleen structuregerelateerde analysis notes toevoegen.
    - Geen indicatoren berekenen.
    - Geen BUY/HOLD/IGNORE beslissingen nemen.
    """

    def analyze(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 0

        latest_close = indicators.get("latest_close")
        recent_high = indicators.get("recent_high_20")
        recent_low = indicators.get("recent_low_20")
        previous_high = indicators.get("previous_high_20")
        previous_low = indicators.get("previous_low_20")

        if (
            latest_close is None
            or recent_high is None
            or recent_low is None
            or previous_high is None
            or previous_low is None
        ):
            result.add_note("Structure: onvoldoende data")
            return 0

        if latest_close >= recent_high:
            score += 40
            result.add_note("Structure: koers breekt boven recente high")

        if recent_high > previous_high:
            score += 30
            result.add_note("Structure: hogere high")

        if recent_low > previous_low:
            score += 30
            result.add_note("Structure: hogere low")

        if latest_close <= recent_low:
            score -= 30
            result.add_note("Structure: koers breekt onder recente low")

        if recent_high <= previous_high and recent_low <= previous_low:
            result.add_note("Structure: geen duidelijke bullish structuur")

        return max(0, min(score, 100))