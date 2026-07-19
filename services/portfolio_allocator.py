from __future__ import annotations

import math
from datetime import UTC, datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import LivePaperCandidate
from models.portfolio_allocation_result import (
    PortfolioAllocationDecision,
    PortfolioAllocationResult,
)
from models.trading_session import TradingSession
from services.risk import RiskContext, RiskManager, RiskProfile
from services.market.fx_rate_service import FxRateService
from services.earnings_calendar_service import EarningsCalendarService
from services.portfolio_concentration_gate import PortfolioConcentrationGate


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
        fx_rate_service: FxRateService | None = None,
        require_live_fx: bool = False,
        concentration_gate: PortfolioConcentrationGate | None = None,
        earnings_calendar_service: EarningsCalendarService | None = None,
    ) -> None:
        self.risk_manager = risk_manager or RiskManager()
        self.fx_rate_service = fx_rate_service
        self.require_live_fx = bool(require_live_fx)
        self.concentration_gate = concentration_gate
        self.earnings_calendar_service = earnings_calendar_service

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
        approved_in_cycle = 0
        pending_positions: list[tuple[str, float]] = []

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

            if approved_in_cycle >= config.max_new_positions_per_cycle:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=(
                            "Maximum new positions per cycle reached."
                        ),
                    )
                )
                continue

            if self.earnings_calendar_service is not None:
                event_decision = self.earnings_calendar_service.evaluate(
                    symbol=candidate.symbol,
                    evaluated_on=datetime.now(UTC).date(),
                    blackout_days=config.earnings_blackout_days,
                )
                if not event_decision.allowed:
                    decisions.append(
                        PortfolioAllocationDecision(
                            candidate=candidate,
                            quantity=0,
                            approved=False,
                            reason=(
                                "Earnings risk gate rejected allocation; "
                                + event_decision.reason
                            ),
                        )
                    )
                    continue

            try:
                fx_rate = self._candidate_fx_rate(
                    symbol=candidate.symbol,
                    base_currency=config.base_currency,
                )
            except ValueError as exc:
                decisions.append(
                    PortfolioAllocationDecision(
                        candidate=candidate,
                        quantity=0,
                        approved=False,
                        reason=f"Risk gate rejected allocation; {exc}",
                    )
                )
                continue

            entry_value_base = entry_price * fx_rate

            quantity = self._calculate_quantity(
                available_cash=spendable_cash,
                portfolio_equity=equity,
                entry_price=entry_value_base,
                max_position_value=config.max_position_value,
                max_position_size_pct=config.max_position_size_pct,
                remaining_exposure_value=remaining_exposure_value,
            )

            if quantity <= 0:
                if (
                    equity * config.max_position_size_pct
                    < entry_value_base
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
                quantity * entry_value_base,
                2,
            )

            if self.concentration_gate is not None:
                concentration = self.concentration_gate.evaluate(
                    session=session,
                    symbol=candidate.symbol,
                    proposed_value=estimated_value,
                    max_positions_per_market=(
                        config.max_positions_per_market
                    ),
                    max_market_exposure_pct=(
                        config.max_market_exposure_pct
                    ),
                    max_positions_per_sector=(
                        config.max_positions_per_sector
                    ),
                    max_sector_exposure_pct=(
                        config.max_sector_exposure_pct
                    ),
                    max_positions_per_correlation_cluster=(
                        config.max_positions_per_correlation_cluster
                    ),
                    pending_positions=pending_positions,
                )
                if not concentration.allowed:
                    decisions.append(
                        PortfolioAllocationDecision(
                            candidate=candidate,
                            quantity=0,
                            approved=False,
                            reason=(
                                "Concentration gate rejected allocation; "
                                + concentration.reason
                            ),
                        )
                    )
                    continue

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
                quantity * (entry_price - stop_loss) * fx_rate,
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
                    fx_rate_to_base=fx_rate,
                )
            )
            approved_in_cycle += 1
            pending_positions.append(
                (candidate.symbol, estimated_value)
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
                quantity
                * max(entry_price - stop_loss, 0.0)
                * getattr(position, "fx_rate_to_base", 1.0)
            )

        return round(risk_amount / portfolio_equity, 4), None

    def _candidate_fx_rate(
        self,
        *,
        symbol: str,
        base_currency: str,
    ) -> float:
        if self.fx_rate_service is None:
            return 1.0

        normalized_base = base_currency.strip().upper()
        if normalized_base != "EUR":
            raise ValueError("portfolio base currency must be EUR.")

        quote_currency = (
            "EUR"
            if str(symbol).strip().upper().endswith((".AS", ".DE"))
            else "USD"
        )
        fx_rate = self.fx_rate_service.get_rate(
            quote_currency,
            normalized_base,
        )

        if self.require_live_fx and fx_rate.source == "fallback":
            raise ValueError(
                f"validated FX rate unavailable for {quote_currency}/"
                f"{normalized_base}."
            )

        rate = float(fx_rate.rate)
        if not math.isfinite(rate) or rate <= 0:
            raise ValueError(
                f"FX rate for {quote_currency}/{normalized_base} "
                "must be finite and greater than zero."
            )

        return rate

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
