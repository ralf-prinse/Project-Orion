from __future__ import annotations

from datetime import UTC, datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.position_adoption import (
    PositionAdoptionConfig,
    PositionAdoptionRecord,
    PositionAdoptionResult,
)
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession


class PositionAdoptionService:
    """Explicitly adopts existing broker positions into Orion lifecycle.

    The service never invents an original BUY thesis. It creates a new,
    auditable management plan using the same configured stop, target,
    trailing-stop, break-even and time-stop services as Orion positions.
    """

    def __init__(self, config: PositionAdoptionConfig) -> None:
        self.config = config

    def adopt(
        self,
        *,
        session: TradingSession,
        trading_config: LivePaperTradingConfig,
        adopted_at: datetime | None = None,
    ) -> PositionAdoptionResult:
        timestamp = adopted_at or datetime.now(UTC)
        records: list[PositionAdoptionRecord] = []

        for requested_symbol in self.config.allowed_symbols:
            symbol = self._find_position_symbol(
                session=session,
                requested_symbol=requested_symbol,
            )

            if symbol is None:
                records.append(
                    PositionAdoptionRecord(
                        symbol=requested_symbol,
                        adopted=False,
                        reason="Allowed position is not open at the broker.",
                        strategy=self.config.strategy,
                    )
                )
                continue

            has_state = symbol in session.position_states
            has_plan = symbol in session.risk_plans

            if has_state and has_plan:
                continue

            if has_state != has_plan:
                raise ValueError(
                    f"Cannot adopt {symbol}: lifecycle state is incomplete."
                )

            position = session.portfolio.positions[symbol]
            risk_plan = self._build_risk_plan(
                symbol=symbol,
                entry_price=position.entry_price,
                trading_config=trading_config,
            )
            session.risk_plans[symbol] = risk_plan
            session.position_states[symbol] = PositionState(
                symbol=symbol,
                entry_price=position.entry_price,
                current_stop_loss=risk_plan.stop_loss,
                highest_price=max(
                    position.entry_price,
                    position.current_price,
                ),
                current_price=position.current_price,
                opened_at=timestamp,
            )
            records.append(
                PositionAdoptionRecord(
                    symbol=symbol,
                    adopted=True,
                    reason=(
                        "Existing IBKR Paper position adopted explicitly; "
                        "original BUY rationale is unavailable. Managed with "
                        f"{self.config.strategy}."
                    ),
                    strategy=self.config.strategy,
                )
            )

        return PositionAdoptionResult(
            session=session,
            records=tuple(records),
        )

    def _build_risk_plan(
        self,
        *,
        symbol: str,
        entry_price: float,
        trading_config: LivePaperTradingConfig,
    ) -> RiskPlan:
        stop_pct = float(trading_config.stop_loss_percent)
        reward_pct = float(trading_config.take_profit_percent)

        if not 0 < stop_pct < 1:
            raise ValueError("Adoption stop-loss percentage is invalid.")
        if not 0 < reward_pct < 1:
            raise ValueError("Adoption take-profit percentage is invalid.")

        return RiskPlan(
            symbol=symbol,
            entry_price=entry_price,
            stop_loss=round(entry_price * (1 - stop_pct), 6),
            target_1=round(entry_price * (1 + reward_pct / 3), 6),
            target_2=round(entry_price * (1 + 2 * reward_pct / 3), 6),
            target_3=round(entry_price * (1 + reward_pct), 6),
            risk_percent=round(stop_pct * 100, 4),
            reward_percent=round(reward_pct * 100, 4),
            risk_reward_ratio=round(reward_pct / stop_pct, 4),
            confidence=0.0,
            notes=(
                "Explicitly adopted existing IBKR Paper position. Original "
                "BUY rationale unavailable; managed by "
                f"{self.config.strategy}."
            ),
        )

    def _find_position_symbol(
        self,
        *,
        session: TradingSession,
        requested_symbol: str,
    ) -> str | None:
        comparison = self._comparison_symbol(requested_symbol)
        matches = [
            symbol
            for symbol in session.portfolio.positions
            if self._comparison_symbol(symbol) == comparison
        ]

        if len(matches) > 1:
            raise ValueError(
                f"Cannot adopt {requested_symbol}: symbol is ambiguous."
            )

        return matches[0] if matches else None

    def _comparison_symbol(self, symbol: str) -> str:
        normalized = str(symbol).strip().upper()
        return normalized[:-3] if normalized.endswith(".AS") else normalized
