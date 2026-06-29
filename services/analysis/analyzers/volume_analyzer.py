from services.analysis.analyzers.base_analyzer import BaseAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


class VolumeAnalyzer(BaseAnalyzer):
    """
    Analyseert volume op basis van berekende volumegegevens.

    Verantwoordelijkheid:
    - Alleen volumescore bepalen.
    - Alleen volumegerelateerde analysis notes toevoegen.
    - Geen indicatoren berekenen.
    - Geen BUY/HOLD/IGNORE beslissingen nemen.
    """

    def analyze(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 0

        latest_volume = indicators.get("latest_volume")
        average_volume_20 = indicators.get("average_volume_20")
        relative_volume = indicators.get("relative_volume_20")
        volume_trend = indicators.get("volume_trend_20")

        if latest_volume is None or average_volume_20 is None:
            result.add_note("Volume: onvoldoende data")
            return 0

        if average_volume_20 <= 0:
            result.add_note("Volume: ongeldig gemiddeld volume")
            return 0

        if relative_volume is not None:
            if relative_volume >= 1.5:
                score += 50
                result.add_note("Volume: sterke volume bevestiging")
            elif relative_volume >= 1.0:
                score += 35
                result.add_note("Volume: normale volume bevestiging")
            elif relative_volume >= 0.7:
                score += 20
                result.add_note("Volume: matige volume bevestiging")
            else:
                result.add_note("Volume: laag relatief volume")

        if volume_trend is not None:
            if volume_trend > 10:
                score += 30
                result.add_note("Volume: stijgende volumetrend")
            elif volume_trend >= -10:
                score += 20
                result.add_note("Volume: stabiele volumetrend")
            else:
                result.add_note("Volume: dalende volumetrend")

        if latest_volume > average_volume_20:
            score += 20
            result.add_note("Volume: huidig volume boven 20-daags gemiddelde")

        return min(score, 100)