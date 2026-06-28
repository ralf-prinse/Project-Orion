from services.analysis.analyzers.momentum_analyzer import MomentumAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


def test_momentum_analyzer_bullish_momentum():
    indicators = IndicatorResult(symbol="TEST")

    indicators.set("rsi14", 55)
    indicators.set(
        "macd",
        {
            "macd": 2.0,
            "signal": 1.0,
            "histogram": 0.5,
        },
    )

    result = AnalysisResult(symbol="TEST")

    analyzer = MomentumAnalyzer()
    score = analyzer.analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 100
    assert "Momentum: RSI gezond voor swing trade" in result.notes
    assert "Momentum: MACD boven signaallijn" in result.notes
    assert "Momentum: MACD histogram positief" in result.notes

    print("Momentum Analyzer test succesvol afgerond.")
    print(f"Score: {score}")
    print("Notes:")
    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    test_momentum_analyzer_bullish_momentum()