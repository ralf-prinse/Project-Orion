from __future__ import annotations

from datetime import UTC, datetime

from models.strategy.trade_evaluation_snapshot import TradeEvaluationSnapshot


class TradeEvaluationBuilder:
    """
    Bouwt een TradeEvaluationSnapshot vanuit de huidige
    analyse-resultaten.

    BELANGRIJK:

    Deze builder verandert GEEN tradingbeslissingen.

    Hij maakt uitsluitend snapshots die later gebruikt
    worden voor:

    - analyse
    - statistics
    - learning
    - position intelligence
    """

    def build(
        self,
        *,
        symbol: str,
        phase: str,
        conviction: float,
        opportunity_score: float,
        thesis: str,
        market_regime: str,
        trend_score: float,
        momentum_score: float,
        volume_score: float,
        volatility_score: float,
        risk_reward: float,
        strengths: list[str],
        weaknesses: list[str],
        notes: str = "",
    ) -> TradeEvaluationSnapshot:

        return TradeEvaluationSnapshot(
            symbol=symbol,
            timestamp=datetime.now(UTC),
            phase=phase,
            conviction=conviction,
            opportunity_score=opportunity_score,
            thesis=thesis,
            market_regime=market_regime,
            trend_score=trend_score,
            momentum_score=momentum_score,
            volume_score=volume_score,
            volatility_score=volatility_score,
            risk_reward=risk_reward,
            strengths=list(strengths),
            weaknesses=list(weaknesses),
            notes=notes,
        )