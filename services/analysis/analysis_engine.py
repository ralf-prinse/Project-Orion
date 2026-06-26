from services.analysis.indicator_engine import IndicatorEngine
from services.analysis.models import AnalysisResult, IndicatorResult


class AnalysisEngine:
    """
    Centrale technische analyse-engine van Project Orion.

    Sprint 7.1:
    - Roept IndicatorEngine aan.
    - Maakt een AnalysisResult aan.
    - Bevat nog geen echte scorelogica.
    - Vormt de basis voor toekomstige trend-, momentum- en volatility-analyse.
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

        result.add_note("Analysis Engine actief")
        result.add_note("Indicator Engine succesvol aangeroepen")

        if indicators.has("sma20"):
            result.add_note("SMA20 indicator beschikbaar")

        if indicators.has("sma50"):
            result.add_note("SMA50 indicator beschikbaar")

        return result