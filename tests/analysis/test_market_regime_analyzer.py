from services.analysis.analyzers.market_regime_analyzer import MarketRegimeAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


def test_market_regime_analyzer_detects_strong_bullish_trend():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("latest_close", 110)
    indicators.set("sma20", 105)
    indicators.set("sma50", 100)
    indicators.set("ema20", 106)
    indicators.set("ema50", 101)
    indicators.set("adx14", 28)

    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 90
    assert "Market regime: strong bullish trend" in result.notes


def test_market_regime_analyzer_detects_bullish_trend():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("latest_close", 110)
    indicators.set("sma20", 105)
    indicators.set("sma50", 100)
    indicators.set("ema20", 106)
    indicators.set("ema50", 101)
    indicators.set("adx14", 20)

    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 75
    assert "Market regime: bullish trend" in result.notes


def test_market_regime_analyzer_detects_strong_bearish_trend():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("latest_close", 90)
    indicators.set("sma20", 95)
    indicators.set("sma50", 100)
    indicators.set("ema20", 94)
    indicators.set("ema50", 99)
    indicators.set("adx14", 30)

    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 15
    assert "Market regime: strong bearish trend" in result.notes


def test_market_regime_analyzer_detects_bearish_trend():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("latest_close", 90)
    indicators.set("sma20", 95)
    indicators.set("sma50", 100)
    indicators.set("ema20", 94)
    indicators.set("ema50", 99)
    indicators.set("adx14", 20)

    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 30
    assert "Market regime: bearish trend" in result.notes


def test_market_regime_analyzer_detects_sideways_market():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("latest_close", 100)
    indicators.set("sma20", 100)
    indicators.set("sma50", 100)
    indicators.set("ema20", 100)
    indicators.set("ema50", 100)
    indicators.set("adx14", 15)

    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 50
    assert "Market regime: sideways market" in result.notes


def test_market_regime_analyzer_detects_choppy_high_volatility_market():
    indicators = IndicatorResult(symbol="TEST")
    indicators.set("latest_close", 100)
    indicators.set("sma20", 100)
    indicators.set("sma50", 100)
    indicators.set("ema20", 100)
    indicators.set("ema50", 100)
    indicators.set("adx14", 22)
    indicators.set("bollinger", {"band_width": 0.20})

    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 40
    assert "Market regime: choppy high-volatility market" in result.notes


def test_market_regime_analyzer_returns_neutral_when_data_is_incomplete():
    indicators = IndicatorResult(symbol="TEST")
    result = AnalysisResult(symbol="TEST")

    score = MarketRegimeAnalyzer().analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 50
    assert "Market regime: neutral" in result.notes