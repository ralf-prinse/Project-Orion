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

                execution_rejection = (
                    cycle.execution_rejections.get(
                        decision.symbol.strip().upper()
                    )
                )
                if execution_rejection is not None:
                    entries.append(
                        self.build_execution_rejection_entry(
                            decision=decision,
                            reason=execution_rejection,
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

    def build_execution_rejection_entry(
        self,
        decision,
        reason: str,
        cycle_number: int,
        session_id: str,
    ) -> TradeJournalEntry:
        return self._build_entry(
            decision=decision,
            position=None,
            action="EXECUTION_REJECTED",
            cycle_number=cycle_number,
            session_id=session_id,
            recommendation_reason=reason,
        )

    def _build_entry(
        self,
        decision,
        position: PaperPosition | None,
        action: str,
        cycle_number: int,
        session_id: str,
        recommendation_reason: str | None = None,
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

        risk_result = getattr(
            decision,
            "risk_result",
            None,
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
            recommendation_reason=(
                recommendation_reason
                if recommendation_reason is not None
                else decision.reason
            ),
            cycle_number=cycle_number,
            session_id=session_id,
            risk_allowed=(
                risk_result.risk_allowed
                if risk_result is not None
                else None
            ),
            proposed_risk_ratio=(
                risk_result.proposed_risk_ratio
                if risk_result is not None
                else None
            ),
            total_portfolio_risk=(
                risk_result.total_portfolio_risk
                if risk_result is not None
                else None
            ),
            drawdown=(
                risk_result.drawdown
                if risk_result is not None
                else None
            ),
            cash_reserve_after_trade=(
                risk_result.cash_reserve_after_trade
                if risk_result is not None
                else None
            ),
            position_exposure=(
                risk_result.position_exposure
                if risk_result is not None
                else None
            ),
            risk_reasons=(
                tuple(risk_result.reasons)
                if risk_result is not None
                else ()
            ),
            risk_warnings=(
                tuple(risk_result.warnings)
                if risk_result is not None
                else ()
            ),
        )
