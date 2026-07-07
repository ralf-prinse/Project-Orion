from __future__ import annotations

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import LivePaperCandidate
from models.portfolio_allocation_result import (
    PortfolioAllocationDecision,
    PortfolioAllocationResult,
)
from models.trading_session import TradingSession


class PortfolioAllocator:
    """
    Deterministic portfolio allocator.

    Responsibilities
    ----------------
    - Select accepted BUY candidates
    - Respect available cash
    - Respect maximum open positions
    - Respect maximum position value
    - Calculate integer quantities

    Does NOT
    --------
    - Fetch market data
    - Run TradingPipeline
    - Execute trades
    - Mutate TradingSession
    """

    def allocate(
        self,
        session: TradingSession,
        candidates: list[LivePaperCandidate],
        config: LivePaperTradingConfig,
    ) -> PortfolioAllocationResult:
        ranked_candidates = sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        decisions: list[PortfolioAllocationDecision] = []

        available_cash = session.cash
        open_positions = session.open_positions

        for candidate in ranked_candidates:
            if not candidate.accepted:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=candidate.reason,
                    )
                )
                continue

            if candidate.symbol in session.portfolio.positions:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason="Position already open.",
                    )
                )
                continue

            if open_positions >= config.max_open_positions:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason="Maximum open positions reached.",
                    )
                )
                continue

            entry_price = candidate.result.risk_plan.entry_price

            quantity = self._calculate_quantity(
                available_cash=available_cash,
                entry_price=entry_price,
                max_position_value=config.max_position_value,
            )

            if quantity <= 0:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason="Insufficient cash for minimum quantity.",
                    )
                )
                continue

            estimated_value = round(
                quantity * entry_price,
                2,
            )

            decisions.append(
                PortfolioAllocationDecision(
                    candidate=candidate,
                    quantity=quantity,
                    approved=True,
                    reason="Approved allocation.",
                )
            )

            available_cash = round(
                available_cash - estimated_value,
                2,
            )
            open_positions += 1

        return PortfolioAllocationResult(
            decisions=decisions,
        )

    def _calculate_quantity(
        self,
        available_cash: float,
        entry_price: float,
        max_position_value: float,
    ) -> int:
        if available_cash <= 0:
            return 0

        if entry_price <= 0:
            return 0

        available_value = min(
            available_cash,
            max_position_value,
        )

        return int(
            available_value // entry_price
        )