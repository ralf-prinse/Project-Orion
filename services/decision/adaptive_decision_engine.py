from services.decision.decision_models import MarketSignal, TradeDecision


class AdaptiveDecisionEngine:
    """
    Dynamic threshold decision engine.

    Input:
    - MarketSignal

    Output:
    - TradeDecision

    This engine decides BUY / SELL / HOLD only.
    Position sizing is handled separately by PositionSizer.
    """

    def evaluate(self, signal: MarketSignal) -> TradeDecision:
        score = signal.score
        trend = signal.trend
        volatility = signal.volatility
        momentum = signal.momentum

        buy_threshold = 0.70
        sell_threshold = 0.40

        if trend > 0.5:
            buy_threshold -= 0.05
            sell_threshold += 0.05
        elif trend < -0.3:
            buy_threshold += 0.05
            sell_threshold -= 0.05

        if volatility > 0.6:
            buy_threshold += 0.05
            sell_threshold -= 0.05
        elif volatility < 0.3:
            buy_threshold -= 0.05
            sell_threshold += 0.05

        if momentum > 0.7:
            buy_threshold -= 0.05
        elif momentum < 0.3:
            sell_threshold -= 0.05

        if score >= buy_threshold and trend > 0:
            decision = "BUY"
            confidence = min(1.0, score + 0.1)
        elif score <= sell_threshold:
            decision = "SELL"
            confidence = max(0.0, 1.0 - score)
        else:
            decision = "HOLD"
            confidence = 0.5

        return TradeDecision(
            symbol=signal.symbol,
            decision=decision,
            confidence=confidence,
            reason=(
                f"Adaptive decision | score={score:.3f} | "
                f"buy_t={buy_threshold:.2f} | sell_t={sell_threshold:.2f}"
            ),
        )