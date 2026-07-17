from __future__ import annotations

import math

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import LivePaperCandidate
from models.portfolio_allocation_result import (
    PortfolioAllocationDecision,
    PortfolioAllocationResult,
)
from models.trading_session import TradingSession
from services.risk import RiskContext, RiskManager, RiskProfile


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

    def __init__(
        self,
        risk_manager: RiskManager | None = None,
    ) -> None:
        self.risk_manager = risk_manager or RiskManager()

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
        current_portfolio_risk, portfolio_risk_error = (
            self._calculate_current_portfolio_risk(
                session=session,
                portfolio_equity=equity,
            )
        )

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
            stop_loss = candidate.result.risk_plan.stop_loss

            if (
                not math.isfinite(entry_price)
                or not math.isfinite(stop_loss)
                or entry_price <= 0
                or stop_loss <= 0
                or stop_loss >= entry_price
            ):
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=(
                            "Risk gate rejected allocation; "
                            "BUY stop-loss must be greater than zero "
                            "and below entry price."
                        ),
                    )
                )
                continue

            quantity = self._calculate_quantity(
                available_cash=spendable_cash,
                portfolio_equity=equity,
                entry_price=entry_price,
                max_position_value=config.max_position_value,
                max_position_size_pct=config.max_position_size_pct,
                remaining_exposure_value=remaining_exposure_value,
            )

            if quantity <= 0:
                if (
                    equity * config.max_position_size_pct
                    < entry_price
                ):
                    rejection_reason = (
                        "Maximum position exposure does not allow "
                        "a whole share."
                    )
                else:
                    rejection_reason = (
                        "Insufficient cash for minimum quantity."
                    )

                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=rejection_reason,
                    )
                )
                continue

            estimated_value = round(
                quantity * entry_price,
                2,
            )

            if portfolio_risk_error is not None:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=portfolio_risk_error,
                    )
                )
                continue

            proposed_risk_amount = round(
                quantity * (entry_price - stop_loss),
                2,
            )

            risk_result = self.risk_manager.evaluate(
                risk_context=RiskContext(
                    symbol=candidate.symbol,
                    portfolio_value=equity,
                    cash_available=available_cash,
                    current_portfolio_risk=current_portfolio_risk,
                    proposed_position_value=estimated_value,
                    proposed_risk_amount=proposed_risk_amount,
                    peak_portfolio_value=(
                        session.peak_portfolio_value
                        if session.peak_portfolio_value > 0
                        else equity
                    ),
                ),
                risk_profile=RiskProfile(
                    max_risk_per_trade=(
                        config.max_risk_per_trade_pct
                    ),
                    max_portfolio_risk=(
                        config.max_portfolio_risk_pct
                    ),
                    max_drawdown=config.max_drawdown_pct,
                    min_cash_reserve=config.min_cash_reserve_pct,
                    max_position_exposure=(
                        config.max_position_size_pct
                    ),
                ),
            )

            if not risk_result.risk_allowed:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=self._risk_rejection_reason(
                            risk_result.warnings
                        ),
                        risk_result=risk_result,
                    )
                )
                continue

            decisions.append(
                PortfolioAllocationDecision(
                    candidate=candidate,
                    quantity=quantity,
                    approved=True,
                    reason="Approved allocation.",
                    risk_result=risk_result,
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
            current_portfolio_risk = (
                risk_result.total_portfolio_risk
            )

        return PortfolioAllocationResult(
            decisions=decisions,
        )

    def _calculate_current_portfolio_risk(
        self,
        *,
        session: TradingSession,
        portfolio_equity: float,
    ) -> tuple[float, str | None]:
        if portfolio_equity <= 0:
            return 0.0, None

        risk_amount = 0.0

        for symbol, position in session.portfolio.positions.items():
            risk_plan = self._find_symbol_value(
                session.risk_plans,
                symbol,
            )

            if risk_plan is None:
                return 0.0, (
                    "Risk gate rejected allocation; current portfolio "
                    f"risk cannot be calculated because {symbol} has "
                    "no managed RiskPlan."
                )

            position_state = self._find_symbol_value(
                session.position_states,
                symbol,
            )
            stop_loss = (
                position_state.current_stop_loss
                if position_state is not None
                else risk_plan.stop_loss
            )
            entry_price = position.entry_price
            quantity = position.quantity

            if (
                not math.isfinite(entry_price)
                or not math.isfinite(stop_loss)
                or entry_price <= 0
                or stop_loss <= 0
                or quantity <= 0
            ):
                return 0.0, (
                    "Risk gate rejected allocation; current portfolio "
                    f"risk data for {symbol} is invalid."
                )

            risk_amount += (
                quantity * max(entry_price - stop_loss, 0.0)
            )

        return round(risk_amount / portfolio_equity, 4), None

    def _find_symbol_value(self, values: dict, symbol: str):
        comparison_symbol = self._comparison_symbol(symbol)

        for key, value in values.items():
            if self._comparison_symbol(key) == comparison_symbol:
                return value

        return None

    def _comparison_symbol(self, symbol: str) -> str:
        normalized = str(symbol).strip().upper()

        if normalized.endswith(".AS"):
            return normalized[:-3]

        return normalized

    def _risk_rejection_reason(
        self,
        warnings: list[str],
    ) -> str:
        details = " ".join(warnings)

        if not details:
            details = "RiskManager rejected the proposed allocation."

        return f"Risk gate rejected allocation; {details}"

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
