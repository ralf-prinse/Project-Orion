from services.analysis.analysis_engine import AnalysisEngine
from services.analysis.analyzer_registry import AnalyzerDefinition, AnalyzerRegistry
from services.analysis.models import IndicatorResult


class StubIndicatorEngine:
    def calculate(
        self,
        symbol,
        candles,
        benchmark_candles=None,
    ):
        indicators = IndicatorResult(symbol=symbol)
        indicators.set("latest_close", 110)
        indicators.set("sma20", 105)
        indicators.set("sma50", 100)
        indicators.set("ema20", 106)
        indicators.set("ema50", 101)
        indicators.set("adx14", 28)
        indicators.set("relative_strength_20", 8)
        indicators.set("relative_strength_50", 10)
        indicators.set("relative_strength_trend", 2)
        return indicators


class StubAnalyzer:
    def __init__(self, score):
        self.score = score
        self.called = False

    def analyze(self, indicators, result):
        self.called = True
        return self.score


class StubCandlestickAnalyzer:
    def __init__(self, score):
        self.score = score
        self.called = False
        self.received_candles = None

    def analyze(self, indicators, candles, result):
        self.called = True
        self.received_candles = candles
        return self.score


def build_stub_registry(
    trend_analyzer,
    momentum_analyzer,
    volatility_analyzer,
    structure_analyzer,
    volume_analyzer,
    market_regime_analyzer,
    relative_strength_analyzer,
    candlestick_pattern_analyzer,
):
    return AnalyzerRegistry(
        analyzers=[
            AnalyzerDefinition(
                name="trend",
                analyzer=trend_analyzer,
                score_field="trend_score",
            ),
            AnalyzerDefinition(
                name="momentum",
                analyzer=momentum_analyzer,
                score_field="momentum_score",
            ),
            AnalyzerDefinition(
                name="volatility",
                analyzer=volatility_analyzer,
                score_field="volatility_score",
            ),
            AnalyzerDefinition(
                name="structure",
                analyzer=structure_analyzer,
                score_field="structure_score",
            ),
            AnalyzerDefinition(
                name="volume",
                analyzer=volume_analyzer,
                score_field="volume_score",
            ),
            AnalyzerDefinition(
                name="market_regime",
                analyzer=market_regime_analyzer,
                score_field="market_regime_score",
                contributes_to_overall=False,
            ),
            AnalyzerDefinition(
                name="relative_strength",
                analyzer=relative_strength_analyzer,
                score_field="relative_strength_score",
            ),
            AnalyzerDefinition(
                name="candlestick",
                analyzer=candlestick_pattern_analyzer,
                score_field="candlestick_score",
                uses_candles=True,
            ),
        ]
    )


def test_analysis_engine_orchestrates_all_registered_analyzers():
    trend_analyzer = StubAnalyzer(80)
    momentum_analyzer = StubAnalyzer(70)
    volatility_analyzer = StubAnalyzer(60)
    structure_analyzer = StubAnalyzer(50)
    volume_analyzer = StubAnalyzer(40)
    market_regime_analyzer = StubAnalyzer(90)
    relative_strength_analyzer = StubAnalyzer(85)
    candlestick_pattern_analyzer = StubCandlestickAnalyzer(75)

    registry = build_stub_registry(
        trend_analyzer=trend_analyzer,
        momentum_analyzer=momentum_analyzer,
        volatility_analyzer=volatility_analyzer,
        structure_analyzer=structure_analyzer,
        volume_analyzer=volume_analyzer,
        market_regime_analyzer=market_regime_analyzer,
        relative_strength_analyzer=relative_strength_analyzer,
        candlestick_pattern_analyzer=candlestick_pattern_analyzer,
    )

    candles = object()

    engine = AnalysisEngine(
        indicator_engine=StubIndicatorEngine(),
        analyzer_registry=registry,
    )

    result = engine.analyze(
        symbol="TEST",
        candles=candles,
    )

    assert trend_analyzer.called is True
    assert momentum_analyzer.called is True
    assert volatility_analyzer.called is True
    assert structure_analyzer.called is True
    assert volume_analyzer.called is True
    assert market_regime_analyzer.called is True
    assert relative_strength_analyzer.called is True
    assert candlestick_pattern_analyzer.called is True
    assert candlestick_pattern_analyzer.received_candles is candles

    assert result.trend_score == 80
    assert result.momentum_score == 70
    assert result.volatility_score == 60
    assert result.structure_score == 50
    assert result.volume_score == 40
    assert result.market_regime_score == 90
    assert result.relative_strength_score == 85
    assert result.candlestick_score == 75


def test_analysis_engine_calculates_weighted_overall_score():
    registry = build_stub_registry(
        trend_analyzer=StubAnalyzer(80),
        momentum_analyzer=StubAnalyzer(70),
        volatility_analyzer=StubAnalyzer(60),
        structure_analyzer=StubAnalyzer(50),
        volume_analyzer=StubAnalyzer(40),
        market_regime_analyzer=StubAnalyzer(90),
        relative_strength_analyzer=StubAnalyzer(85),
        candlestick_pattern_analyzer=StubCandlestickAnalyzer(75),
    )

    engine = AnalysisEngine(
        indicator_engine=StubIndicatorEngine(),
        analyzer_registry=registry,
    )

    result = engine.analyze(
        symbol="TEST",
        candles=None,
    )

    assert result.overall_score == 67
    assert "Overall technical score: 67" in result.notes


def test_analysis_engine_returns_error_result_when_indicators_fail():
    class FailingIndicatorEngine:
        def calculate(
            self,
            symbol,
            candles,
            benchmark_candles=None,
        ):
            indicators = IndicatorResult(symbol=symbol)
            indicators.set("error", "Test indicator error")
            return indicators

    engine = AnalysisEngine(
        indicator_engine=FailingIndicatorEngine(),
    )

    result = engine.analyze(
        symbol="TEST",
        candles=None,
    )

    assert result.overall_score == 0
    assert result.market_regime_score == 0
    assert result.relative_strength_score == 0
    assert result.candlestick_score == 0
    assert "Test indicator error" in result.notes