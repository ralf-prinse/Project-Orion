import pandas as pd

from services.analysis.analyzers.candlestick_pattern_analyzer import (
    CandlestickPatternAnalyzer,
)
from services.analysis.models import AnalysisResult, IndicatorResult


def _candles(rows):
    return pd.DataFrame(rows)


def _analyze(rows):
    indicators = IndicatorResult(symbol="TEST")
    result = AnalysisResult(symbol="TEST")

    score = CandlestickPatternAnalyzer().analyze(
        indicators=indicators,
        candles=_candles(rows),
        result=result,
    )

    return score, result


def test_candlestick_analyzer_detects_hammer():
    score, result = _analyze(
        [
            {"Open": 100, "High": 102, "Low": 99, "Close": 101},
            {"Open": 100, "High": 101, "Low": 90, "Close": 102},
        ]
    )

    assert score == 70
    assert "Candlestick: bullish pattern detected (hammer)" in result.notes


def test_candlestick_analyzer_detects_shooting_star():
    score, result = _analyze(
        [
            {"Open": 101, "High": 102, "Low": 99, "Close": 100},
            {"Open": 102, "High": 112, "Low": 101, "Close": 100},
        ]
    )

    assert score == 30
    assert "Candlestick: bearish pattern detected (shooting star)" in result.notes


def test_candlestick_analyzer_detects_bullish_engulfing():
    score, result = _analyze(
        [
            {"Open": 105, "High": 106, "Low": 99, "Close": 100},
            {"Open": 99, "High": 108, "Low": 98, "Close": 106},
        ]
    )

    assert score == 70
    assert "Candlestick: bullish pattern detected (bullish engulfing)" in result.notes


def test_candlestick_analyzer_detects_bearish_engulfing():
    score, result = _analyze(
        [
            {"Open": 100, "High": 106, "Low": 99, "Close": 105},
            {"Open": 106, "High": 107, "Low": 98, "Close": 99},
        ]
    )

    assert score == 30
    assert "Candlestick: bearish pattern detected (bearish engulfing)" in result.notes


def test_candlestick_analyzer_detects_piercing_line():
    score, result = _analyze(
        [
            {"Open": 110, "High": 111, "Low": 99, "Close": 100},
            {"Open": 98, "High": 108, "Low": 97, "Close": 106},
        ]
    )

    assert score == 70
    assert "Candlestick: bullish pattern detected (piercing line)" in result.notes


def test_candlestick_analyzer_detects_dark_cloud_cover():
    score, result = _analyze(
        [
            {"Open": 100, "High": 111, "Low": 99, "Close": 110},
            {"Open": 112, "High": 113, "Low": 101, "Close": 104},
        ]
    )

    assert score == 30
    assert "Candlestick: bearish pattern detected (dark cloud cover)" in result.notes


def test_candlestick_analyzer_returns_neutral_without_pattern():
    score, result = _analyze(
        [
            {"Open": 100, "High": 103, "Low": 99, "Close": 102},
            {"Open": 102, "High": 104, "Low": 101, "Close": 103},
        ]
    )

    assert score == 50
    assert "Candlestick: no major pattern detected" in result.notes


def test_candlestick_analyzer_returns_neutral_with_insufficient_data():
    indicators = IndicatorResult(symbol="TEST")
    result = AnalysisResult(symbol="TEST")

    score = CandlestickPatternAnalyzer().analyze(
        indicators=indicators,
        candles=pd.DataFrame(
            [{"Open": 100, "High": 102, "Low": 99, "Close": 101}]
        ),
        result=result,
    )

    assert score == 50
    assert "Candlestick: insufficient candle data" in result.notes