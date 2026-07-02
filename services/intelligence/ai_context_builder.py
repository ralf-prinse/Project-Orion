from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class AIContext:
    """
    Unified AI-ready trading context.

    This is the FIRST layer designed for LLM / AI reasoning.
    """

    symbol: str

    # market signals
    pressure_score: float
    buy_pressure: float
    sell_pressure: float
    strength: float

    # intelligence context
    regime: str
    volatility: str
    risk_score: float

    # decision layer
    decision: str
    confidence: float
    reason: str

    # execution layer
    position_size: float
    expected_risk: float

    # raw feature vector
    features: Dict[str, Any]


class AIContextBuilder:
    """
    Converts pipeline output → AI reasoning object.
    """

    def build(self, pipeline_output: dict) -> AIContext:

        return AIContext(
            symbol=pipeline_output["symbol"],

            pressure_score=pipeline_output["pressure_score"],
            buy_pressure=pipeline_output["buy_pressure"],
            sell_pressure=pipeline_output["sell_pressure"],
            strength=pipeline_output["strength"],

            regime=pipeline_output["regime"],
            volatility=pipeline_output["volatility"],
            risk_score=pipeline_output["risk_score"],

            decision=pipeline_output["decision"],
            confidence=pipeline_output["confidence"],
            reason=pipeline_output["reason"],

            position_size=pipeline_output["position_size"],
            expected_risk=pipeline_output["expected_risk"],

            features=pipeline_output["features"],
        )