from __future__ import annotations

from models.opportunity_ranking import (
    OpportunityRankFactor,
    OpportunityRanking,
)
from models.trading_pipeline_result import TradingPipelineResult


class OpportunityRankingEngine:
    """Ranks Orion candidates for short trades with a 24-48 hour horizon.

    The engine does not approve, reject, size or execute trades. It only
    creates one deterministic cross-candidate comparison score.
    """

    def rank(self, result: TradingPipelineResult) -> OpportunityRanking:
        thesis = result.investment_thesis
        factor_map = {
            factor.name: factor.score
            for factor in (thesis.factors if thesis is not None else ())
        }

        factors = (
            self._factor(
                "active_confidence",
                self._clamp01(result.confidence),
                0.20,
                "Confidence of the active deterministic decision.",
            ),
            self._factor(
                "momentum",
                factor_map.get("momentum", 0.5),
                0.23,
                "Short-horizon continuation requires strong momentum.",
            ),
            self._factor(
                "pressure_confirmation",
                factor_map.get("pressure_confirmation", 0.5),
                0.17,
                "Buy pressure should confirm the expected move.",
            ),
            self._factor(
                "volatility_opportunity",
                self._volatility_opportunity(
                    factor_map.get("volatility_quality", 0.5)
                ),
                0.12,
                "Volatility must offer movement without becoming unstable.",
            ),
            self._factor(
                "market_regime",
                factor_map.get("market_regime", 0.4),
                0.10,
                "The broader regime should support a short long trade.",
            ),
            self._factor(
                "risk_reward",
                factor_map.get(
                    "risk_reward",
                    self._clamp01(result.risk_plan.risk_reward_ratio / 3.0),
                ),
                0.13,
                "Expected reward must justify the planned downside.",
            ),
            self._factor(
                "entry_timing",
                self._entry_timing_score(factor_map),
                0.05,
                "Entry timing penalizes overextended short-term setups.",
            ),
        )

        raw_score = sum(factor.contribution for factor in factors)
        decision_multiplier = {
            "BUY": 1.0,
            "HOLD": 0.65,
            "SELL": 0.20,
        }.get(str(result.decision).upper(), 0.35)
        score = round(self._clamp01(raw_score * decision_multiplier) * 100, 2)

        strengths = tuple(
            factor.rationale for factor in factors if factor.score >= 0.70
        )
        weaknesses = tuple(
            factor.rationale for factor in factors if factor.score <= 0.40
        )
        band = self._band(score)

        return OpportunityRanking(
            symbol=result.symbol.strip().upper(),
            score=score,
            rank_band=band,
            factors=factors,
            strengths=strengths,
            weaknesses=weaknesses,
            summary=(
                f"{band} 48-hour opportunity with score {score:.2f}/100; "
                f"decision={result.decision}."
            ),
        )

    def _entry_timing_score(self, factors: dict[str, float]) -> float:
        rsi = factors.get("rsi_context", 0.5)
        trend = factors.get("trend", 0.5)
        momentum = factors.get("momentum", 0.5)
        return self._clamp01((rsi * 0.45) + (trend * 0.25) + (momentum * 0.30))

    def _volatility_opportunity(self, quality: float) -> float:
        value = self._clamp01(quality)
        # Medium, controlled volatility is most useful for a 24-48h trade.
        return self._clamp01(1.0 - abs(value - 0.75) * 1.5)

    def _factor(
        self,
        name: str,
        score: float,
        weight: float,
        rationale: str,
    ) -> OpportunityRankFactor:
        normalized = self._clamp01(score)
        return OpportunityRankFactor(
            name=name,
            score=round(normalized, 4),
            weight=weight,
            contribution=round(normalized * weight, 4),
            rationale=rationale,
        )

    def _band(self, score: float) -> str:
        if score >= 75.0:
            return "TOP"
        if score >= 60.0:
            return "STRONG"
        if score >= 45.0:
            return "WATCH"
        return "WEAK"

    def _clamp01(self, value: float) -> float:
        return max(0.0, min(float(value), 1.0))
