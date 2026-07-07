from __future__ import annotations

from models.risk_plan import RiskPlan
from models.risk_context import RiskContext

class AdaptiveRiskEngine:
    """
    Builds adaptive stop-loss and take-profit levels.

    Responsibilities
    ----------------
    - Calculate an adaptive stop-loss
    - Calculate three adaptive profit targets
    - Calculate risk/reward metrics

    Does NOT:
    - Generate BUY/HOLD/SELL decisions
    - Execute trades
    - Persist data
    - Render UI
    """

        symbol = context.symbol
        entry_price = context.entry_price
        confidence = context.confidence
        risk_score = context.risk_score
        volatility = context.volatility
        regime = context.regime
        market = context.market_structure


    def build(
        self,
        context: RiskContext,
    ):

        entry = max(0.0, float(entry_price))
        confidence_value = max(0.0, min(1.0, float(confidence)))
        risk_value = max(0.0, float(risk_score))

        if entry <= 0:
            return RiskPlan(
                symbol=str(symbol).strip().upper(),
                entry_price=0.0,
                stop_loss=0.0,
                target_1=0.0,
                target_2=0.0,
                target_3=0.0,
                risk_percent=0.0,
                reward_percent=0.0,
                risk_reward_ratio=0.0,
                confidence=confidence_value,
                notes="Invalid entry price.",
            )

        stop_percent = self._stop_percent(
            confidence=confidence_value,
            risk_score=risk_value,
            volatility=volatility,
            regime=regime,
        )

        reward_multiplier = self._reward_multiplier(
            confidence=confidence_value,
            volatility=volatility,
            regime=regime,
        )

        target_1_percent = stop_percent * reward_multiplier
        target_2_percent = target_1_percent * 1.6
        target_3_percent = target_1_percent * 2.3

        stop_loss = round(entry * (1 - stop_percent), 2)
        target_1 = round(entry * (1 + target_1_percent), 2)
        target_2 = round(entry * (1 + target_2_percent), 2)
        target_3 = round(entry * (1 + target_3_percent), 2)

        risk_percent = round(stop_percent * 100, 2)
        reward_percent = round(target_1_percent * 100, 2)

        risk_reward_ratio = (
            round(target_1_percent / stop_percent, 2)
            if stop_percent > 0
            else 0.0
        )

        return RiskPlan(
            symbol=str(symbol).strip().upper(),
            entry_price=round(entry, 2),
            stop_loss=stop_loss,
            target_1=target_1,
            target_2=target_2,
            target_3=target_3,
            risk_percent=risk_percent,
            reward_percent=reward_percent,
            risk_reward_ratio=risk_reward_ratio,
            confidence=confidence_value,
            notes=self._notes(
                confidence=confidence_value,
                risk_score=risk_value,
                volatility=volatility,
                regime=regime,
            ),
        )

    def _stop_percent(
        self,
        confidence: float,
        risk_score: float,
        volatility: str,
        regime: str,
    ) -> float:
        base = 0.035

        volatility_factor = {
            "LOW": -0.008,
            "NORMAL": 0.0,
            "MEDIUM": 0.004,
            "HIGH": 0.012,
        }.get(str(volatility).strip().upper(), 0.0)

        regime_factor = {
            "BULL": -0.004,
            "SIDEWAYS": 0.004,
            "BEAR": 0.012,
        }.get(str(regime).strip().upper(), 0.0)

        confidence_factor = (1.0 - confidence) * 0.02
        risk_factor = min(risk_score, 0.05) * 0.5

        stop = (
            base
            + volatility_factor
            + regime_factor
            + confidence_factor
            + risk_factor
        )

        return max(0.018, min(0.085, stop))

    def _reward_multiplier(
        self,
        confidence: float,
        volatility: str,
        regime: str,
    ) -> float:
        base = 2.0

        confidence_bonus = confidence * 0.8

        volatility_adjustment = {
            "LOW": -0.15,
            "NORMAL": 0.0,
            "MEDIUM": 0.1,
            "HIGH": 0.25,
        }.get(str(volatility).strip().upper(), 0.0)

        regime_adjustment = {
            "BULL": 0.35,
            "SIDEWAYS": -0.15,
            "BEAR": -0.4,
        }.get(str(regime).strip().upper(), 0.0)

        multiplier = (
            base
            + confidence_bonus
            + volatility_adjustment
            + regime_adjustment
        )

        return max(1.4, min(3.6, multiplier))

    def _notes(
        self,
        confidence: float,
        risk_score: float,
        volatility: str,
        regime: str,
    ) -> str:
        return (
            "Adaptive risk plan | "
            f"confidence={confidence:.2f} | "
            f"risk={risk_score:.4f} | "
            f"volatility={str(volatility).strip().upper()} | "
            f"regime={str(regime).strip().upper()}"
        )