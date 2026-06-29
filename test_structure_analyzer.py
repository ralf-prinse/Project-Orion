from services.analysis.analyzers.structure_analyzer import StructureAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


def test_structure_analyzer_bullish_structure():
    indicators = IndicatorResult(symbol="TEST")

    indicators.set("latest_close", 125.0)
    indicators.set("recent_high_20", 125.0)
    indicators.set("recent_low_20", 110.0)
    indicators.set("previous_high_20", 120.0)
    indicators.set("previous_low_20", 100.0)

    result = AnalysisResult(symbol="TEST")

    analyzer = StructureAnalyzer()
    score = analyzer.analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 100
    assert "Structure: koers breekt boven recente high" in result.notes
    assert "Structure: hogere high" in result.notes
    assert "Structure: hogere low" in result.notes

    print("Structure Analyzer test succesvol afgerond.")
    print(f"Score: {score}")
    print("Notes:")
    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    test_structure_analyzer_bullish_structure()