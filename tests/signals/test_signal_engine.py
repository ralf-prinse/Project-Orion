from services.analysis.models import AnalysisResult
from services.signals.models import Signal
from services.signals.signal_engine import SignalEngine
from services.signals.signal_registry import SignalAnalyzerDefinition, SignalRegistry


class StubSignalAnalyzer:
    def __init__(self):
        self.called = False

    def analyze(
        self,
        analysis_result,
        signal_result,
    ):
        self.called = True
        signal_result.signal = Signal.WATCH
        signal_result.confidence = 55
        signal_result.bullish_score = 60
        signal_result.bearish_score = 20
        signal_result.neutral_score = 20
        signal_result.add_note("Stub signal analyzer executed.")
        return signal_result


def make_analysis_result(
    symbol="TEST",
    overall_score=0,
    trend_score=0,
    momentum_score=0,
    volatility_score=0,
    structure_score=0,
    volume_score=0,
    market_regime_score=0,
    relative_strength_score=0,
    candlestick_score=0,
):
    return AnalysisResult(
        symbol=symbol,
        overall_score=overall_score,
        trend_score=trend_score,
        momentum_score=momentum_score,
        volatility_score=volatility_score,
        structure_score=structure_score,
        volume_score=volume_score,
        market_regime_score=market_regime_score,
        relative_strength_score=relative_strength_score,
        candlestick_score=candlestick_score,
    )


def test_signal_engine_generates_buy_signal():
    analysis_result = make_analysis_result(
        overall_score=82,
        trend_score=80,
        momentum_score=70,
        structure_score=72,
        volume_score=60,
        relative_strength_score=75,
        candlestick_score=55,
    )

    engine = SignalEngine()

    result = engine.generate(analysis_result)

    assert result.symbol == "TEST"
    assert result.signal == Signal.BUY
    assert result.confidence == 71
    assert result.bullish_score == 71
    assert result.bearish_score == 24
    assert result.neutral_score == 29
    assert "BUY signal detected by EntrySignalAnalyzer." in result.notes
    assert "Final signal: BUY with confidence 71" in result.notes


def test_signal_engine_generates_watch_signal():
    analysis_result = make_analysis_result(
        overall_score=65,
        trend_score=62,
        momentum_score=58,
        structure_score=57,
        volume_score=40,
        relative_strength_score=60,
        candlestick_score=20,
    )

    engine = SignalEngine()

    result = engine.generate(analysis_result)

    assert result.symbol == "TEST"
    assert result.signal == Signal.WATCH
    assert result.confidence == 52
    assert result.bullish_score == 52
    assert "WATCH signal detected by EntrySignalAnalyzer." in result.notes
    assert "Final signal: WATCH with confidence 52" in result.notes


def test_signal_engine_generates_sell_signal():
    analysis_result = make_analysis_result(
        overall_score=30,
        trend_score=25,
        momentum_score=30,
        structure_score=35,
        volume_score=45,
        relative_strength_score=40,
        candlestick_score=30,
    )

    engine = SignalEngine()

    result = engine.generate(analysis_result)

    assert result.symbol == "TEST"
    assert result.signal == Signal.SELL
    assert result.confidence == 70
    assert result.bearish_score == 70
    assert "SELL signal detected by EntrySignalAnalyzer." in result.notes
    assert "Final signal: SELL with confidence 70" in result.notes


def test_signal_engine_generates_ignore_signal_when_no_threshold_matches():
    analysis_result = make_analysis_result(
        overall_score=50,
        trend_score=50,
        momentum_score=50,
        structure_score=50,
        volume_score=50,
        relative_strength_score=50,
        candlestick_score=50,
    )

    engine = SignalEngine()

    result = engine.generate(analysis_result)

    assert result.symbol == "TEST"
    assert result.signal == Signal.IGNORE
    assert result.confidence == 50
    assert result.bullish_score == 50
    assert result.bearish_score == 50
    assert result.neutral_score == 50
    assert "No actionable entry signal detected." in result.notes
    assert "Final signal: IGNORE with confidence 50" in result.notes


def test_signal_engine_orchestrates_registered_signal_analyzers():
    stub_analyzer = StubSignalAnalyzer()

    registry = SignalRegistry(
        analyzers=[
            SignalAnalyzerDefinition(
                name="stub",
                analyzer=stub_analyzer,
            )
        ]
    )

    analysis_result = AnalysisResult(symbol="TEST")

    engine = SignalEngine(
        signal_registry=registry,
    )

    result = engine.generate(analysis_result)

    assert stub_analyzer.called is True
    assert result.symbol == "TEST"
    assert result.signal == Signal.WATCH
    assert result.confidence == 55
    assert result.bullish_score == 60
    assert result.bearish_score == 20
    assert result.neutral_score == 20
    assert "Stub signal analyzer executed." in result.notes
    assert "Final signal: WATCH with confidence 55" in result.notes