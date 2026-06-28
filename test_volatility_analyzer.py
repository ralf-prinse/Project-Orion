from services.analysis.analyzers.volatility_analyzer import VolatilityAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


def test_volatility_analyzer_healthy_volatility():
    indicators = IndicatorResult(symbol="TEST")

    indicators.set("atr14", 4.0)
    indicators.set(
        "bollinger",
        {
            "middle": 100.0,
            "upper": 110.0,
            "lower": 90.0,
            "width": 12.0,
        },
    )

    result = AnalysisResult(symbol="TEST")

    analyzer = VolatilityAnalyzer()
    score = analyzer.analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 100
    assert "Volatility: ATR beschikbaar en geldig" in result.notes
    assert "Volatility: Bollinger width gezond" in result.notes

    print("Volatility Analyzer test succesvol afgerond.")
    print(f"Score: {score}")
    print("Notes:")
    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    test_volatility_analyzer_healthy_volatility()