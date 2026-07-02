from services.decision.decision_models import (
    DecisionInput,
    TradeDecision,
)

from services.decision.position_sizing import PositionSizer


class DecisionEngine:
    """
    Core decision engine.
    NO UI, NO STATE, ONLY PURE LOGIC.
    """

    def __init__(self):
        self.sizer = PositionSizer()

    def evaluate(self, data: DecisionInput) -> TradeDecision:
        signal = data.signal

        position_size = self.sizer.calculate_position_size(data)

        # decision logic (deterministic)
        if signal.score >= 0.7 and signal.trend > 0:
            decision = "BUY"
            confidence = min(signal.score / 100, 1.0)

        elif signal.score <= 0.4:
            decision = "SELL"
            confidence = 1 - (signal.score / 100)

        else:
            decision = "HOLD"
            confidence = 0.5

        risk = signal.volatility * position_size

        reason = self._build_reason(signal, decision)

        return TradeDecision(
            symbol=signal.symbol,
            decision=decision,
            confidence=confidence,
            position_size=position_size,
            expected_risk=risk,
            reason=reason,
        )

    def _build_reason(self, signal, decision: str) -> str:
        return (
            f"{decision} based on score={signal.score}, "
            f"trend={signal.trend}, volatility={signal.volatility}"
        )