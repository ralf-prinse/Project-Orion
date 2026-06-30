from services.analysis.analyzer_registry import AnalyzerRegistry
from services.analysis.config.analysis_weights import ALL_WEIGHTS
from services.analysis.indicator_engine import IndicatorEngine
from services.analysis.models import AnalysisResult, IndicatorResult


class AnalysisEngine:
    """
    Centrale technische analyse-engine van Project Orion.

    Sprint 8.1.1:
    - Roept IndicatorEngine aan.
    - Haalt analyzers op uit AnalyzerRegistry.
    - Voert analyzers uit in deterministische volgorde.
    - Geeft raw candledata alleen door aan analyzers die dat nodig hebben.
    - Gebruikt centrale configuratie voor scorewegingen.
    - Berekent overall score intern.

    AnalysisEngine bevat geen analyse-logica.
    De engine orkestreert uitsluitend IndicatorEngine en geregistreerde analyzers.
    """

    def __init__(
        self,
        indicator_engine: IndicatorEngine | None = None,
        analyzer_registry: AnalyzerRegistry | None = None,
    ):
        self.indicator_engine = indicator_engine or IndicatorEngine()
        self.analyzer_registry = analyzer_registry or AnalyzerRegistry()

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
            candles=candles,
            indicators=indicators,
        )

    def _build_analysis_result(
        self,
        symbol: str,
        candles,
        indicators: IndicatorResult,
    ) -> AnalysisResult:
        result = AnalysisResult(symbol=symbol)

        if indicators.has("error"):
            result.add_note(indicators.get("error"))
            return result

        for analyzer_definition in self.analyzer_registry.get_analyzers():
            score = self._run_analyzer(
                analyzer_definition=analyzer_definition,
                indicators=indicators,
                candles=candles,
                result=result,
            )

            setattr(
                result,
                analyzer_definition.score_field,
                score,
            )

        result.overall_score = self._calculate_overall_score(result)

        result.add_note(f"Overall technical score: {result.overall_score}")

        return result

    def _run_analyzer(
        self,
        analyzer_definition,
        indicators: IndicatorResult,
        candles,
        result: AnalysisResult,
    ) -> int:
        """
        Voert één analyzer uit.

        Sommige analyzers, zoals CandlestickPatternAnalyzer, hebben raw candles
        nodig. Indicator-gebaseerde analyzers ontvangen alleen IndicatorResult.
        """
        if analyzer_definition.uses_candles:
            return analyzer_definition.analyzer.analyze(
                indicators=indicators,
                candles=candles,
                result=result,
            )

        return analyzer_definition.analyzer.analyze(
            indicators=indicators,
            result=result,
        )

    def _calculate_overall_score(
        self,
        result: AnalysisResult,
    ) -> int:
        """
        Berekent de overall technische score met centrale configuratie.

        Alleen analyzers die expliciet bijdragen aan de overall score worden
        meegenomen. MarketRegimeAnalyzer blijft daardoor marktcontext en telt
        bewust niet mee in de technische totaalscore.
        """
        weighted_score = 0.0

        for analyzer_definition in self.analyzer_registry.get_overall_score_analyzers():
            score = getattr(result, analyzer_definition.score_field)
            weight = ALL_WEIGHTS[analyzer_definition.name]
            weighted_score += score * weight

        return int(round(weighted_score))