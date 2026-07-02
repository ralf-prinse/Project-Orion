from services.intelligence.intelligence_models import (
    IndicatorPack,
    MarketIntelligenceSnapshot,
)

from services.intelligence.feature_builder import FeatureBuilder


class MarketIntelligenceEngine:
    """
    Transforms raw indicators → structured market intelligence.
    NO trading decisions here.
    """

    def __init__(self):
        self.feature_builder = FeatureBuilder()

    def analyze(self, data: IndicatorPack) -> MarketIntelligenceSnapshot:

        # 1. normalize inputs
        rsi_n = self._norm(data.rsi)
        trend = self._clamp(data.trend, -1, 1)
        vol = self._norm(data.volatility)
        mom = self._norm(data.momentum)

        # 2. composite score
        composite = (
            0.35 * trend +
            0.25 * mom +
            0.25 * rsi_n +
            0.15 * (1 - vol)
        )

        # 3. regime detection
        if trend > 0.4:
            regime = "BULL"
        elif trend < -0.3:
            regime = "BEAR"
        else:
            regime = "SIDEWAYS"

        # 4. volatility state
        if vol < 0.3:
            vol_state = "LOW"
        elif vol < 0.7:
            vol_state = "MEDIUM"
        else:
            vol_state = "HIGH"

        # 5. confidence (simple stability proxy)
        confidence = 1 - abs(vol - 0.5)

        # 6. risk score
        risk_score = vol * (1 + abs(trend))

        # 7. AI feature vector
        features = self.feature_builder.build(data)

        return MarketIntelligenceSnapshot(
            symbol=data.symbol,
            composite_score=round(composite, 4),
            confidence=round(confidence, 4),
            regime=regime,
            volatility_state=vol_state,
            trend_strength=trend,
            momentum_strength=mom,
            risk_score=round(risk_score, 4),
            ai_feature_vector=features,
        )

    def _norm(self, value: float) -> float:
        return max(0.0, min(value / 100.0, 1.0))

    def _clamp(self, value: float, min_v: float, max_v: float) -> float:
        return max(min_v, min(max_v, value))