from services.analysis.analyzers.momentum_analyzer import MomentumAnalyzer
from services.analysis.analyzers.structure_analyzer import StructureAnalyzer
from services.analysis.analyzers.trend_analyzer import TrendAnalyzer
from services.analysis.analyzers.volatility_analyzer import VolatilityAnalyzer
from services.analysis.indicator_engine import IndicatorEngine
from services.analysis.models import AnalysisResult, IndicatorResult


class AnalysisEngine:
    """
    Centrale technische analyse-engine van Project Orion.

    Sprint 7.7:
    - Roept IndicatorEngine aan.
    - Delegeert trendscore aan TrendAnalyzer.
    - Delegeert momentumscore aan MomentumAnalyzer.
    - Delegeert volatilityscore aan VolatilityAnalyzer.
    - Delegeert structurescore aan StructureAnalyzer.
    - Berekent overall score intern.
    """

    def __init__(
        self,
        indicator_engine: IndicatorEngine | None = None,
        trend_analyzer: TrendAnalyzer | None = None,
        momentum_analyzer: MomentumAnalyzer | None = None,
        volatility_analyzer: VolatilityAnalyzer | None = None,
        structure_analyzer: StructureAnalyzer | None = None,
    ):
        self.indicator_engine = indicator_engine or IndicatorEngine()
        self.trend_analyzer = trend_analyzer or TrendAnalyzer()
        self.momentum_analyzer = momentum_analyzer or MomentumAnalyzer()
        self.volatility_analyzer = volatility_analyzer or VolatilityAnalyzer()
        self.structure_analyzer = structure_analyzer or StructureAnalyzer()

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

        result.trend_score = self.trend_analyzer.analyze(
            indicators=indicators,
            result=result,
        )

        result.momentum_score = self.momentum_analyzer.analyze(
            indicators=indicators,
            result=result,
        )

        result.volatility_score = self.volatility_analyzer.analyze(
            indicators=indicators,
            result=result,
        )

        result.structure_score = self.structure_analyzer.analyze(
            indicators=indicators,
            result=result,
        )

        result.overall_score = self._calculate_overall_score(result)

        result.add_note(f"Overall technical score: {result.overall_score}")

        return result

    def _calculate_overall_score(
        self,
        result: AnalysisResult,
    ) -> int:
        weighted_score = (
            result.trend_score * 0.35
            + result.momentum_score * 0.30
            + result.volatility_score * 0.20
            + result.structure_score * 0.15
        )

        return int(round(weighted_score))