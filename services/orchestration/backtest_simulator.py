from typing import Dict, Any


class BacktestSimulator:
    """
    Deterministic backtest simulator.

    Uses Orion pipeline output:
    - pressure_score
    - confidence
    - strength
    - position_size
    - expected_risk
    """

    def __init__(self, fee_rate: float = 0.001, slippage_rate: float = 0.0005):
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate

    def simulate_trade(self, trade: Dict[str, Any]) -> Dict[str, Any]:
        pressure_score = trade.get("pressure_score", 0.0)
        confidence = trade.get("confidence", 0.0)
        strength = trade.get("strength", 0.0)
        position_size = trade.get("position_size", 0.0)
        expected_risk = trade.get("expected_risk", 0.0)
        decision = trade.get("decision", "HOLD")

        if decision == "HOLD" or position_size <= 0:
            return {
                "gross_pnl": 0.0,
                "fees": 0.0,
                "slippage": 0.0,
                "net_pnl": 0.0,
                "outcome": "NO_TRADE",
            }

        edge = pressure_score * confidence * strength

        gross_pnl = position_size * edge * 0.005

        if confidence < 0.55:
            gross_pnl = -expected_risk

        if decision == "SELL":
            gross_pnl *= 0.75

        fees = position_size * self.fee_rate
        slippage = position_size * self.slippage_rate

        net_pnl = gross_pnl - fees - slippage

        return {
            "gross_pnl": round(gross_pnl, 6),
            "fees": round(fees, 6),
            "slippage": round(slippage, 6),
            "net_pnl": round(net_pnl, 6),
            "outcome": "WIN" if net_pnl > 0 else "LOSS",
        }