from typing import Dict


class AIExplainer:
    """
    Converts AIContext → human-readable reasoning.
    This is the "WHY" layer of Orion.
    """

    def explain(self, ai_context) -> Dict[str, str]:

        reasons = []

        # -------------------------
        # 1. DECISION BASIS
        # -------------------------
        if ai_context.decision == "BUY":
            reasons.append(
                f"Strong BUY signal with pressure_score={ai_context.pressure_score:.3f}"
            )

        elif ai_context.decision == "SELL":
            reasons.append(
                f"Strong SELL signal with pressure imbalance"
            )

        else:
            reasons.append(
                f"Market indecision (HOLD zone)"
            )

        # -------------------------
        # 2. MARKET REGIME
        # -------------------------
        if ai_context.regime == "BULL":
            reasons.append("Bullish market regime supports long positions")

        elif ai_context.regime == "BEAR":
            reasons.append("Bearish regime increases downside risk")

        else:
            reasons.append("Sideways regime reduces conviction")

        # -------------------------
        # 3. VOLATILITY CONTEXT
        # -------------------------
        if ai_context.volatility == "LOW":
            reasons.append("Low volatility favors stable entry")

        elif ai_context.volatility == "HIGH":
            reasons.append("High volatility increases risk")

        # -------------------------
        # 4. PRESSURE ANALYSIS
        # -------------------------
        if ai_context.buy_pressure > ai_context.sell_pressure:
            reasons.append("Buy pressure dominates sell pressure")
        else:
            reasons.append("Sell pressure dominates or balances market")

        # -------------------------
        # 5. CONFIDENCE LEVEL
        # -------------------------
        if ai_context.confidence > 0.75:
            reasons.append("High confidence decision")
        elif ai_context.confidence < 0.5:
            reasons.append("Low confidence, caution advised")

        return {
            "summary": reasons[0],
            "details": reasons,
        }