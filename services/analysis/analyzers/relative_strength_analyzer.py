from services.analysis.analyzers.base_analyzer import BaseAnalyzer
from services.analysis.models import AnalysisResult, IndicatorResult


class RelativeStrengthAnalyzer(BaseAnalyzer):
    """
    Analyseert relatieve sterkte ten opzichte van een benchmark.

    Deze analyzer bepaalt of een aandeel sterker of zwakker presteert
    dan de bredere markt. De benchmark wordt later in de pipeline
    aangeleverd, bijvoorbeeld SPY.
    """

    def analyze(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        relative_strength_20 = indicators.get("relative_strength_20")
        relative_strength_50 = indicators.get("relative_strength_50")
        relative_strength_trend = indicators.get("relative_strength_trend")

        if relative_strength_20 is None and relative_strength_50 is None:
            result.add_note("Relative strength: insufficient benchmark data")
            return 50

        score = 50

        if relative_strength_20 is not None:
            score += self._score_relative_strength_20(relative_strength_20)

        if relative_strength_50 is not None:
            score += self._score_relative_strength_50(relative_strength_50)

        if relative_strength_trend is not None:
            score += self._score_relative_strength_trend(relative_strength_trend)

        score = max(0, min(100, score))

        self._add_note(
            result=result,
            score=score,
        )

        return score

    def _score_relative_strength_20(
        self,
        relative_strength_20: float,
    ) -> int:
        if relative_strength_20 >= 10:
            return 25

        if relative_strength_20 >= 5:
            return 15

        if relative_strength_20 >= 0:
            return 5

        if relative_strength_20 <= -10:
            return -25

        if relative_strength_20 <= -5:
            return -15

        return -5

    def _score_relative_strength_50(
        self,
        relative_strength_50: float,
    ) -> int:
        if relative_strength_50 >= 15:
            return 20

        if relative_strength_50 >= 7:
            return 12

        if relative_strength_50 >= 0:
            return 5

        if relative_strength_50 <= -15:
            return -20

        if relative_strength_50 <= -7:
            return -12

        return -5

    def _score_relative_strength_trend(
        self,
        relative_strength_trend: float,
    ) -> int:
        if relative_strength_trend >= 5:
            return 10

        if relative_strength_trend > 0:
            return 5

        if relative_strength_trend <= -5:
            return -10

        if relative_strength_trend < 0:
            return -5

        return 0

    def _add_note(
        self,
        result: AnalysisResult,
        score: int,
    ) -> None:
        if score >= 80:
            result.add_note("Relative strength: strong market outperformance")
            return

        if score >= 65:
            result.add_note("Relative strength: positive market outperformance")
            return

        if score >= 45:
            result.add_note("Relative strength: neutral versus market")
            return

        if score >= 30:
            result.add_note("Relative strength: market underperformance")
            return

        result.add_note("Relative strength: strong market underperformance")