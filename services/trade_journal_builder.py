from __future__ import annotations

from datetime import datetime

from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.trade_journal_entry import TradeJournalEntry


class TradeJournalBuilder:
    """
    Builds deterministic trade journal entries from an autonomous
    paper trading result.

    This service does not analyse performance.
    It only transforms execution history into long-term memory records.
    """

    def build(
        self,
        result: AutonomousPaperTradingResult,
        session_id: str = "default-session",
    ) -> list[TradeJournalEntry]:
        entries: list[TradeJournalEntry] = []

        for cycle_index, cycle in enumerate(
            result.cycle_results,
            start=1,
        ):
            for decision in cycle.allocation.decisions:
                candidate = decision.candidate
                pipeline_result = candidate.result
                risk_plan = pipeline_result.risk_plan

                position = result.session.portfolio.positions.get(
                    decision.symbol
                )

                unrealized_profit_loss = (
                    position.unrealized_profit_loss
                    if position is not None
                    else 0.0
                )

                current_price = (
                    position.current_price
                    if position is not None
                    else risk_plan.entry_price
                )

                market_intelligence = (
                    pipeline_result.market_intelligence
                )

                regime = getattr(
                    market_intelligence,
                    "regime",
                    "UNKNOWN",
                )

                volatility = getattr(
                    market_intelligence,
                    "volatility_state",
                    "UNKNOWN",
                )

                entries.append(
                    TradeJournalEntry(
                        timestamp=datetime.now(),
                        symbol=decision.symbol,
                        action=(
                            "OPEN_POSITION"
                            if decision.approved
                            else "REJECTED"
                        ),
                        decision=pipeline_result.decision,
                        confidence=pipeline_result.confidence,
                        score=candidate.score,
                        entry_price=risk_plan.entry_price,
                        exit_price=None,
                        quantity=decision.quantity,
                        invested_amount=decision.estimated_value,
                        realized_profit_loss=0.0,
                        unrealized_profit_loss=unrealized_profit_loss,
                        expected_risk=pipeline_result.expected_risk,
                        regime=regime,
                        volatility=volatility,
                        ai_summary=str(pipeline_result.explanation),
                        recommendation_reason=decision.reason,
                        cycle_number=cycle_index,
                        session_id=session_id,
                    )
                )

        return entries