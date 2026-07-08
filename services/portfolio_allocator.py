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
    - Respect cash reserve
    - Respect maximum portfolio exposure
    - Respect maximum position size
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
        exposure_value = session.portfolio.positions_value
        equity = session.equity

        max_exposure_value = round(
            equity * config.max_portfolio_exposure,
            2,
        )

        cash_reserve = round(
            equity * config.min_cash_reserve_pct,
            2,
        )

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

            remaining_exposure_value = round(
                max_exposure_value - exposure_value,
                2,
            )

            spendable_cash = round(
                available_cash - cash_reserve,
                2,
            )

            if remaining_exposure_value <= 0:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason="Maximum portfolio exposure reached.",
                    )
                )
                continue

            if spendable_cash <= 0:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason="Cash reserve reached.",
                    )
                )
                continue

            entry_price = candidate.result.risk_plan.entry_price

            quantity = self._calculate_quantity(
                available_cash=spendable_cash,
                portfolio_equity=equity,
                entry_price=entry_price,
                max_position_value=config.max_position_value,
                max_position_size_pct=config.max_position_size_pct,
                remaining_exposure_value=remaining_exposure_value,
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

            exposure_value = round(
                exposure_value + estimated_value,
                2,
            )

            open_positions += 1

        return PortfolioAllocationResult(
            decisions=decisions,
        )

    def _calculate_quantity(
        self,
        available_cash: float,
        portfolio_equity: float,
        entry_price: float,
        max_position_value: float,
        max_position_size_pct: float,
        remaining_exposure_value: float,
    ) -> int:
        if available_cash <= 0:
            return 0

        if portfolio_equity <= 0:
            return 0

        if entry_price <= 0:
            return 0

        max_position_by_pct = round(
            portfolio_equity * max_position_size_pct,
            2,
        )

        available_value = min(
            available_cash,
            max_position_value,
            max_position_by_pct,
            remaining_exposure_value,
        )

        return int(
            available_value // entry_price
        )