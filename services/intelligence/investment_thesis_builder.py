from __future__ import annotations

from models.investment_thesis import InvestmentThesis, ThesisFactor
from models.risk_plan import RiskPlan
from services.intelligence.intelligence_models import (
    IndicatorPack,
    MarketIntelligenceSnapshot,
)
from services.intelligence.signal_fusion_engine import FusedSignal


class InvestmentThesisBuilder:
    """
    Builds a transparent deterministic investment thesis in shadow mode.

    The builder reuses existing Orion output. It does not replace the active
    BUY/HOLD/SELL decision yet. This allows thesis quality to be measured
    before it is allowed to influence execution.
    """

    def build(
        self,
        indicators: IndicatorPack,
        fused: FusedSignal,
        intelligence: MarketIntelligenceSnapshot,
        risk_plan: RiskPlan,
    ) -> InvestmentThesis:
        factors = (
            self._factor(
                "trend",
                self._clamp01(fused.trend),
                0.22,
                self._trend_rationale(fused.trend),
            ),
            self._factor(
                "momentum",
                self._clamp01(fused.momentum),
                0.18,
                self._momentum_rationale(fused.momentum),
            ),
            self._factor(
                "pressure_confirmation",
                self._pressure_score(fused),
                0.15,
                self._pressure_rationale(fused),
            ),
            self._factor(
                "market_regime",
                self._regime_score(intelligence.regime),
                0.15,
                f"Detected market regime: {intelligence.regime}.",
            ),
            self._factor(
                "rsi_context",
                self._rsi_score(indicators.rsi, fused.trend),
                0.10,
                self._rsi_rationale(indicators.rsi, fused.trend),
            ),
            self._factor(
                "volatility_quality",
                self._volatility_score(intelligence.volatility_state),
                0.08,
                f"Volatility state: {intelligence.volatility_state}.",
            ),
            self._factor(
                "risk_reward",
                self._risk_reward_score(risk_plan.risk_reward_ratio),
                0.12,
                (
                    "Risk/reward ratio is "
                    f"{risk_plan.risk_reward_ratio:.2f}."
                ),
            ),
        )

        quality = self._clamp01(sum(item.contribution for item in factors))
        conviction = round(quality * 100.0, 2)
        stance = self._stance(conviction, factors)

        supporting = tuple(
            item.rationale for item in factors if item.score >= 0.65
        )
        risks = tuple(
            item.rationale for item in factors if item.score <= 0.40
        )
        invalidations = self._invalidation_conditions(
            indicators=indicators,
            risk_plan=risk_plan,
            intelligence=intelligence,
        )

        return InvestmentThesis(
            symbol=str(indicators.symbol).strip().upper(),
            stance=stance,
            conviction=conviction,
            quality=round(quality, 4),
            factors=factors,
            supporting_reasons=supporting,
            risk_reasons=risks,
            invalidation_conditions=invalidations,
            summary=(
                f"{stance} thesis with {conviction:.2f}/100 conviction; "
                f"regime={intelligence.regime}, "
                f"risk/reward={risk_plan.risk_reward_ratio:.2f}."
            ),
        )

    def _factor(
        self,
        name: str,
        score: float,
        weight: float,
        rationale: str,
    ) -> ThesisFactor:
        normalized = self._clamp01(score)
        return ThesisFactor(
            name=name,
            score=round(normalized, 4),
            weight=weight,
            contribution=round(normalized * weight, 4),
            rationale=rationale,
        )

    def _pressure_score(self, fused: FusedSignal) -> float:
        edge = fused.buy_pressure - fused.sell_pressure
        return self._clamp01((edge + 1.0) / 2.0)

    def _regime_score(self, regime: str) -> float:
        return {
            "BULL": 1.0,
            "SIDEWAYS": 0.5,
            "BEAR": 0.0,
        }.get(str(regime).strip().upper(), 0.4)

    def _volatility_score(self, state: str) -> float:
        return {
            "LOW": 0.75,
            "MEDIUM": 1.0,
            "HIGH": 0.25,
        }.get(str(state).strip().upper(), 0.5)

    def _risk_reward_score(self, ratio: float) -> float:
        return self._clamp01(float(ratio) / 3.0)

    def _rsi_score(self, rsi: float, trend: float) -> float:
        value = max(0.0, min(float(rsi), 100.0))

        if value >= 80.0:
            return 0.15
        if value >= 70.0:
            return 0.45 if trend > 0.0 else 0.25
        if value >= 50.0:
            return 0.85 if trend > 0.0 else 0.55
        if value >= 35.0:
            return 0.55
        return 0.30

    def _stance(
        self,
        conviction: float,
        factors: tuple[ThesisFactor, ...],
    ) -> str:
        factor_map = {item.name: item.score for item in factors}
        trend = factor_map["trend"]
        risk_reward = factor_map["risk_reward"]
        regime = factor_map["market_regime"]

        if (
            conviction >= 68.0
            and trend >= 0.55
            and risk_reward >= 0.50
            and regime > 0.0
        ):
            return "BUY"

        if conviction >= 48.0 and trend >= 0.40:
            return "WATCH"

        return "AVOID"

    def _invalidation_conditions(
        self,
        indicators: IndicatorPack,
        risk_plan: RiskPlan,
        intelligence: MarketIntelligenceSnapshot,
    ) -> tuple[str, ...]:
        conditions = [
            f"Price closes below the planned stop at {risk_plan.stop_loss:.2f}.",
        ]

        support = float(indicators.market_structure.support)
        if support > 0.0:
            conditions.append(
                f"Market structure breaks below support at {support:.2f}."
            )

        if intelligence.regime != "BEAR":
            conditions.append("Market regime changes to BEAR.")

        conditions.append("Trend or momentum loses deterministic confirmation.")
        return tuple(conditions)

    def _trend_rationale(self, trend: float) -> str:
        if trend >= 0.55:
            return "Trend strongly supports a long thesis."
        if trend > 0.0:
            return "Trend is positive but not yet strong."
        return "Trend does not support a long thesis."

    def _momentum_rationale(self, momentum: float) -> str:
        if momentum >= 0.65:
            return "Momentum confirms continued upside pressure."
        if momentum >= 0.45:
            return "Momentum is neutral to moderately positive."
        return "Momentum is weak and reduces thesis quality."

    def _pressure_rationale(self, fused: FusedSignal) -> str:
        edge = fused.buy_pressure - fused.sell_pressure
        if edge >= 0.25:
            return "Buy pressure clearly exceeds sell pressure."
        if edge > 0.0:
            return "Buy pressure only slightly exceeds sell pressure."
        return "Sell pressure equals or exceeds buy pressure."

    def _rsi_rationale(self, rsi: float, trend: float) -> str:
        if rsi >= 80.0:
            return "RSI is extremely high and signals overextension risk."
        if rsi >= 70.0:
            return "RSI confirms strength but also raises overbought risk."
        if 50.0 <= rsi < 70.0 and trend > 0.0:
            return "RSI supports healthy bullish momentum."
        if rsi < 35.0:
            return "RSI is weak; reversal is not confirmed by RSI alone."
        return "RSI provides limited directional confirmation."

    def _clamp01(self, value: float) -> float:
        return max(0.0, min(float(value), 1.0))
