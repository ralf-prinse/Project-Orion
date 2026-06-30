from services.analysis.analyzers.market_regime_analyzer import MarketRegimeAnalyzer
from services.analysis.analyzers.momentum_analyzer import MomentumAnalyzer
from services.analysis.analyzers.structure_analyzer import StructureAnalyzer
from services.analysis.analyzers.trend_analyzer import TrendAnalyzer
from services.analysis.analyzers.volatility_analyzer import VolatilityAnalyzer
from services.analysis.analyzers.volume_analyzer import VolumeAnalyzer
from services.analysis.indicator_engine import IndicatorEngine
from services.analysis.models import AnalysisResult, IndicatorResult


class AnalysisEngine:
    """
    Centrale technische analyse-engine van Project Orion.

    Sprint 7.9:
    - Roept IndicatorEngine aan.
    - Delegeert trendscore aan TrendAnalyzer.
    - Delegeert momentumscore aan MomentumAnalyzer.
    - Delegeert volatilityscore aan VolatilityAnalyzer.
    - Delegeert structurescore aan StructureAnalyzer.
    - Delegeert volumescore aan VolumeAnalyzer.
    - Delegeert market regime score aan MarketRegimeAnalyzer.
    - Berekent overall score intern.

    MarketRegimeAnalyzer levert marktcontext en wordt bewust niet meegenomen
    in de overall technische score om dubbele weging te voorkomen.
    """

    def __init__(
        self,
        indicator_engine: IndicatorEngine | None = None,
        trend_analyzer: TrendAnalyzer | None = None,
        momentum_analyzer: MomentumAnalyzer | None = None,
        volatility_analyzer: VolatilityAnalyzer | None = None,
        structure_analyzer: StructureAnalyzer | None = None,
        volume_analyzer: VolumeAnalyzer | None = None,
        market_regime_analyzer: MarketRegimeAnalyzer | None = None,
    ):
        self.indicator_engine = indicator_engine or IndicatorEngine()
        self.trend_analyzer = trend_analyzer or TrendAnalyzer()
        self.momentum_analyzer = momentum_analyzer or MomentumAnalyzer()
        self.volatility_analyzer = volatility_analyzer or VolatilityAnalyzer()
        self.structure_analyzer = structure_analyzer or StructureAnalyzer()
        self.volume_analyzer = volume_analyzer or VolumeAnalyzer()
        self.market_regime_analyzer = (
            market_regime_analyzer or MarketRegimeAnalyzer()
        )

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

        result.volume_score = self.volume_analyzer.analyze(
            indicators=indicators,
            result=result,
        )

        result.market_regime_score = self.market_regime_analyzer.analyze(
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
        """
        Berekent de overall technische score.

        MarketRegimeAnalyzer levert context over het huidige markttype,
        maar wordt bewust nog niet meegenomen in de overall score om
        dubbele weging van bestaande technische kenmerken te voorkomen.

        De Market Regime-score zal in toekomstige sprints worden gebruikt
        door de Signal Engine en Decision Engine.
        """

        weighted_score = (
            result.trend_score * 0.30
            + result.momentum_score * 0.25
            + result.volatility_score * 0.15
            + result.structure_score * 0.15
            + result.volume_score * 0.15
        )

        return int(round(weighted_score))