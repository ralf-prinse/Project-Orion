from services.analysis.analyzers.relative_strength_analyzer import (
    RelativeStrengthAnalyzer,
)
from services.analysis.models import AnalysisResult, IndicatorResult


def test_relative_strength_analyzer_detects_strong_outperformance():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("relative_strength_20", 12)
    indicators.set("relative_strength_50", 18)
    indicators.set("relative_strength_trend", 6)

    result = AnalysisResult(symbol="TEST")

    score = RelativeStrengthAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 100
    assert "Relative strength: strong market outperformance" in result.notes


def test_relative_strength_analyzer_detects_positive_outperformance():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("relative_strength_20", 6)
    indicators.set("relative_strength_50", 8)
    indicators.set("relative_strength_trend", 2)

    result = AnalysisResult(symbol="TEST")

    score = RelativeStrengthAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 82
    assert "Relative strength: strong market outperformance" in result.notes


def test_relative_strength_analyzer_detects_neutral_strength():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("relative_strength_20", 1)
    indicators.set("relative_strength_50", 1)
    indicators.set("relative_strength_trend", 0)

    result = AnalysisResult(symbol="TEST")

    score = RelativeStrengthAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 60
    assert "Relative strength: neutral versus market" in result.notes


def test_relative_strength_analyzer_detects_underperformance():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("relative_strength_20", -6)
    indicators.set("relative_strength_50", -8)
    indicators.set("relative_strength_trend", -2)

    result = AnalysisResult(symbol="TEST")

    score = RelativeStrengthAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 18
    assert "Relative strength: strong market underperformance" in result.notes


def test_relative_strength_analyzer_detects_strong_underperformance():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("relative_strength_20", -12)
    indicators.set("relative_strength_50", -18)
    indicators.set("relative_strength_trend", -6)

    result = AnalysisResult(symbol="TEST")

    score = RelativeStrengthAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 0
    assert "Relative strength: strong market underperformance" in result.notes


def test_relative_strength_analyzer_returns_neutral_when_benchmark_data_missing():
    indicators = IndicatorResult(symbol="TEST")
    result = AnalysisResult(symbol="TEST")

    score = RelativeStrengthAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 50
    assert "Relative strength: insufficient benchmark data" in result.notes