from services.analysis.analyzers.volume_analyzer import VolumeAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


def test_volume_analyzer_strong_volume_confirmation():
    indicators = IndicatorResult(symbol="TEST")

    indicators.set("latest_volume", 1_800_000)
    indicators.set("average_volume_20", 1_000_000)
    indicators.set("relative_volume_20", 1.8)
    indicators.set("volume_trend_20", 15.0)

    result = AnalysisResult(symbol="TEST")

    analyzer = VolumeAnalyzer()
    score = analyzer.analyze(
        indicators=indicators,
        result=result,
    )

    assert score == 100
    assert "Volume: sterke volume bevestiging" in result.notes
    assert "Volume: stijgende volumetrend" in result.notes
    assert "Volume: huidig volume boven 20-daags gemiddelde" in result.notes

    print("Volume Analyzer test succesvol afgerond.")
    print(f"Score: {score}")
    print("Notes:")
    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    test_volume_analyzer_strong_volume_confirmation()