from services.intelligence.intelligence_models import IndicatorPack


class FeatureBuilder:
    """
    Builds AI-ready feature vectors.
    """

    def build(self, data: IndicatorPack) -> list[float]:
        return [
            self._norm(data.rsi),
            self._norm_signed(data.trend),
            self._norm(data.volatility),
            self._norm(data.momentum),
        ]

    def _norm(self, value: float) -> float:
        return max(0.0, min(value / 100.0, 1.0))

    def _norm_signed(self, value: float) -> float:
        return max(-1.0, min(value, 1.0))