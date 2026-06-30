from services.analysis.analyzers.market_regime_analyzer import MarketRegimeAnalyzer
from services.analysis.analyzers.momentum_analyzer import MomentumAnalyzer
from services.analysis.analyzers.relative_strength_analyzer import (
    RelativeStrengthAnalyzer,
)
from services.analysis.analyzers.structure_analyzer import StructureAnalyzer
from services.analysis.analyzers.trend_analyzer import TrendAnalyzer
from services.analysis.analyzers.volatility_analyzer import VolatilityAnalyzer
from services.analysis.analyzers.volume_analyzer import VolumeAnalyzer
from services.analysis.config.analysis_weights import ALL_WEIGHTS
from services.analysis.indicator_engine import IndicatorEngine
from services.analysis.models import AnalysisResult, IndicatorResult


class AnalysisEngine:
    """
    Centrale technische analyse-engine van Project Orion.

    Sprint 8.0.1:
    - Roept IndicatorEngine aan.
    - Delegeert alle analysegebieden aan gespecialiseerde analyzers.
    - Gebruikt centrale configuratie voor scorewegingen.
    - Berekent overall score intern.

    MarketRegimeAnalyzer levert marktcontext en wordt bewust niet meegenomen
    in de overall technische score om dubbele weging te voorkomen.

    RelativeStrengthAnalyzer levert marktvergelijking en wordt meegenomen
    als technische kwaliteitscomponent.
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
        relative_strength_analyzer: RelativeStrengthAnalyzer | None = None,
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
        self.relative_strength_analyzer = (
            relative_strength_analyzer or RelativeStrengthAnalyzer()
        )

    def analyze(
        self,
        symbol: str,
        candles,
        benchmark_candles=None,
    ) -> AnalysisResult:
        indicators = self.indicator_engine.calculate(
            symbol=symbol,
            candles=candles,
            benchmark_candles=benchmark_candles,
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

        result.relative_strength_score = self.relative_strength_analyzer.analyze(
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
        Berekent de overall technische score met centrale configuratie.

        MarketRegimeAnalyzer levert context over het huidige markttype,
        maar wordt bewust niet meegenomen in de overall score om
        dubbele weging van bestaande technische kenmerken te voorkomen.
        """

        weighted_score = (
            result.trend_score * ALL_WEIGHTS["trend"]
            + result.momentum_score * ALL_WEIGHTS["momentum"]
            + result.volatility_score * ALL_WEIGHTS["volatility"]
            + result.structure_score * ALL_WEIGHTS["structure"]
            + result.volume_score * ALL_WEIGHTS["volume"]
            + result.relative_strength_score * ALL_WEIGHTS["relative_strength"]
        )

        return int(round(weighted_score))