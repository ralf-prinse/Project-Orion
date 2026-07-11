from __future__ import annotations

from datetime import datetime

from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.paper_position import PaperPosition
from models.trade_journal_entry import TradeJournalEntry


class TradeJournalBuilder:
    """
    Builds immutable journal entries from allocation decisions.

    Decision journal:
    - one entry for every allocation decision
    - action is APPROVED or REJECTED

    Trade journal:
    - OPEN_POSITION is written only after TradingCycle confirms execution
    - CLOSE_POSITION is written by the exit runtime

    This service contains no trading or persistence logic.
    """

    def build(
        self,
        result: AutonomousPaperTradingResult,
        session_id: str = "default-session",
    ) -> list[TradeJournalEntry]:
        """
        Backward-compatible alias for decision-journal entries.
        """

        return self.build_decision_entries(
            result=result,
            session_id=session_id,
        )

    def build_decision_entries(
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
                position = result.session.portfolio.positions.get(
                    decision.symbol
                )

                entries.append(
                    self.build_decision_entry(
                        decision=decision,
                        position=position,
                        cycle_number=cycle_index,
                        session_id=session_id,
                    )
                )

        return entries

    def build_decision_entry(
        self,
        decision,
        position: PaperPosition | None,
        cycle_number: int,
        session_id: str,
    ) -> TradeJournalEntry:
        return self._build_entry(
            decision=decision,
            position=position,
            action=(
                "APPROVED"
                if decision.approved
                else "REJECTED"
            ),
            cycle_number=cycle_number,
            session_id=session_id,
        )

    def build_open_trade_entry(
        self,
        decision,
        position: PaperPosition,
        cycle_number: int,
        session_id: str,
    ) -> TradeJournalEntry:
        return self._build_entry(
            decision=decision,
            position=position,
            action="OPEN_POSITION",
            cycle_number=cycle_number,
            session_id=session_id,
        )

    def _build_entry(
        self,
        decision,
        position: PaperPosition | None,
        action: str,
        cycle_number: int,
        session_id: str,
    ) -> TradeJournalEntry:
        candidate = decision.candidate
        pipeline_result = candidate.result
        risk_plan = pipeline_result.risk_plan

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

        return TradeJournalEntry(
            timestamp=datetime.now(),
            symbol=decision.symbol,
            action=action,
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
            cycle_number=cycle_number,
            session_id=session_id,
        )
