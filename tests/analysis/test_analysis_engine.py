from services.analysis.analysis_engine import AnalysisEngine
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


def test_analysis_engine_orchestrates_all_analyzers():
    trend_analyzer = StubAnalyzer(80)
    momentum_analyzer = StubAnalyzer(70)
    volatility_analyzer = StubAnalyzer(60)
    structure_analyzer = StubAnalyzer(50)
    volume_analyzer = StubAnalyzer(40)
    market_regime_analyzer = StubAnalyzer(90)
    relative_strength_analyzer = StubAnalyzer(85)

    engine = AnalysisEngine(
        indicator_engine=StubIndicatorEngine(),
        trend_analyzer=trend_analyzer,
        momentum_analyzer=momentum_analyzer,
        volatility_analyzer=volatility_analyzer,
        structure_analyzer=structure_analyzer,
        volume_analyzer=volume_analyzer,
        market_regime_analyzer=market_regime_analyzer,
        relative_strength_analyzer=relative_strength_analyzer,
    )

    result = engine.analyze(
        symbol="TEST",
        candles=None,
    )

    assert trend_analyzer.called is True
    assert momentum_analyzer.called is True
    assert volatility_analyzer.called is True
    assert structure_analyzer.called is True
    assert volume_analyzer.called is True
    assert market_regime_analyzer.called is True
    assert relative_strength_analyzer.called is True

    assert result.trend_score == 80
    assert result.momentum_score == 70
    assert result.volatility_score == 60
    assert result.structure_score == 50
    assert result.volume_score == 40
    assert result.market_regime_score == 90
    assert result.relative_strength_score == 85


def test_analysis_engine_calculates_weighted_overall_score():
    engine = AnalysisEngine(
        indicator_engine=StubIndicatorEngine(),
        trend_analyzer=StubAnalyzer(80),
        momentum_analyzer=StubAnalyzer(70),
        volatility_analyzer=StubAnalyzer(60),
        structure_analyzer=StubAnalyzer(50),
        volume_analyzer=StubAnalyzer(40),
        market_regime_analyzer=StubAnalyzer(90),
        relative_strength_analyzer=StubAnalyzer(85),
    )

    result = engine.analyze(
        symbol="TEST",
        candles=None,
    )

    assert result.overall_score == 65
    assert "Overall technical score: 65" in result.notes


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
    assert "Test indicator error" in result.notes