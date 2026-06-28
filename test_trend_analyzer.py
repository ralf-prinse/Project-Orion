from services.analysis.analyzers.trend_analyzer import TrendAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


def test_trend_analyzer_bullish_trend():
    indicators = IndicatorResult(symbol="TEST")

    indicators.set("sma20", 120)
    indicators.set("sma50", 100)
    indicators.set("ema20", 121)
    indicators.set("ema50", 101)
    indicators.set(
        "adx14",
        {
            "adx": 30,
            "plus_di": 25,
            "minus_di": 10,
        },
    )

    result = AnalysisResult(symbol="TEST")

    analyzer = TrendAnalyzer()
    score = analyzer.analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 100
    assert result.notes
    assert "Trend: SMA20 boven SMA50" in result.notes
    assert "Trend: EMA20 boven EMA50" in result.notes
    assert "Trend: ADX bevestigt voldoende trendsterkte" in result.notes
    assert "Trend: +DI boven -DI" in result.notes

    print("Trend Analyzer test succesvol afgerond.")
    print(f"Score: {score}")
    print("Notes:")
    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    test_trend_analyzer_bullish_trend()