from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from models.trading_session import TradingSession


@dataclass(frozen=True)
class TradingSessionIntegrityResult:
    valid: bool
    errors: tuple[str, ...]
    managed_symbols: tuple[str, ...]
    legacy_symbols: tuple[str, ...]


class TradingSessionIntegrityError(ValueError):
    def __init__(self, errors: tuple[str, ...]):
        self.errors = errors

        details = "\n".join(
            f"- {error}"
            for error in errors
        )

        super().__init__(
            "TradingSession integrity validation failed:\n"
            + details
        )


class TradingSessionIntegrityService:
    """
    Audits structural consistency of a TradingSession.

    A managed position must have both PositionState and RiskPlan.
    A legacy position may temporarily have neither.

    The service never mutates session state and contains no trading logic.
    """

    def audit(
        self,
        session: TradingSession,
    ) -> TradingSessionIntegrityResult:
        errors: list[str] = []
        managed_symbols: list[str] = []
        legacy_symbols: list[str] = []

        self._validate_session_metadata(
            session=session,
            errors=errors,
        )

        position_symbols = set(session.portfolio.positions)
        state_symbols = set(session.position_states)
        risk_plan_symbols = set(session.risk_plans)

        self._validate_position_entries(
            session=session,
            errors=errors,
        )
        self._validate_state_entries(
            session=session,
            position_symbols=position_symbols,
            errors=errors,
        )
        self._validate_risk_plan_entries(
            session=session,
            position_symbols=position_symbols,
            errors=errors,
        )

        for symbol in sorted(position_symbols):
            has_state = symbol in state_symbols
            has_risk_plan = symbol in risk_plan_symbols

            if has_state != has_risk_plan:
                missing = (
                    "RiskPlan"
                    if has_state
                    else "PositionState"
                )
                errors.append(
                    f"{symbol}: managed lifecycle is incomplete; "
                    f"{missing} is missing."
                )
                continue

            if not has_state:
                legacy_symbols.append(symbol)
                continue

            managed_symbols.append(symbol)

            position = session.portfolio.positions[symbol]
            state = session.position_states[symbol]
            risk_plan = session.risk_plans[symbol]

            if not self._same_number(
                position.entry_price,
                state.entry_price,
            ):
                errors.append(
                    f"{symbol}: PaperPosition.entry_price "
                    "does not match PositionState.entry_price."
                )

            if not self._same_number(
                position.entry_price,
                risk_plan.entry_price,
            ):
                errors.append(
                    f"{symbol}: PaperPosition.entry_price "
                    "does not match RiskPlan.entry_price."
                )

            if not self._same_number(
                position.current_price,
                state.current_price,
            ):
                errors.append(
                    f"{symbol}: PaperPosition.current_price "
                    "does not match PositionState.current_price."
                )

            if state.highest_price < state.current_price:
                errors.append(
                    f"{symbol}: PositionState.highest_price "
                    "is below current_price."
                )

        return TradingSessionIntegrityResult(
            valid=not errors,
            errors=tuple(errors),
            managed_symbols=tuple(managed_symbols),
            legacy_symbols=tuple(legacy_symbols),
        )

    def validate(
        self,
        session: TradingSession,
    ) -> None:
        result = self.audit(session)

        if not result.valid:
            raise TradingSessionIntegrityError(
                result.errors,
            )

    def _validate_session_metadata(
        self,
        session: TradingSession,
        errors: list[str],
    ) -> None:
        if not str(session.name).strip():
            errors.append(
                "TradingSession.name is required."
            )

        if not str(session.status).strip():
            errors.append(
                "TradingSession.status is required."
            )

        if not isfinite(float(session.portfolio.cash)):
            errors.append(
                "PaperPortfolio.cash must be finite."
            )

    def _validate_position_entries(
        self,
        session: TradingSession,
        errors: list[str],
    ) -> None:
        for key, position in session.portfolio.positions.items():
            normalized_key = self._normalize_symbol(key)
            normalized_symbol = self._normalize_symbol(
                position.symbol
            )

            if key != normalized_key:
                errors.append(
                    f"{key}: portfolio key must be normalized "
                    f"as {normalized_key}."
                )

            if normalized_key != normalized_symbol:
                errors.append(
                    f"{key}: portfolio key does not match "
                    f"PaperPosition.symbol {normalized_symbol}."
                )

    def _validate_state_entries(
        self,
        session: TradingSession,
        position_symbols: set[str],
        errors: list[str],
    ) -> None:
        for key, state in session.position_states.items():
            normalized_key = self._normalize_symbol(key)
            normalized_symbol = self._normalize_symbol(
                state.symbol
            )

            if key != normalized_key:
                errors.append(
                    f"{key}: PositionState key must be "
                    f"normalized as {normalized_key}."
                )

            if normalized_key != normalized_symbol:
                errors.append(
                    f"{key}: PositionState key does not match "
                    f"PositionState.symbol {normalized_symbol}."
                )

            if key not in position_symbols:
                errors.append(
                    f"{key}: orphan PositionState has no "
                    "matching PaperPosition."
                )

    def _validate_risk_plan_entries(
        self,
        session: TradingSession,
        position_symbols: set[str],
        errors: list[str],
    ) -> None:
        for key, risk_plan in session.risk_plans.items():
            normalized_key = self._normalize_symbol(key)
            normalized_symbol = self._normalize_symbol(
                risk_plan.symbol
            )

            if key != normalized_key:
                errors.append(
                    f"{key}: RiskPlan key must be normalized "
                    f"as {normalized_key}."
                )

            if normalized_key != normalized_symbol:
                errors.append(
                    f"{key}: RiskPlan key does not match "
                    f"RiskPlan.symbol {normalized_symbol}."
                )

            if key not in position_symbols:
                errors.append(
                    f"{key}: orphan RiskPlan has no "
                    "matching PaperPosition."
                )

    def _normalize_symbol(
        self,
        symbol: str,
    ) -> str:
        return str(symbol).strip().upper()

    def _same_number(
        self,
        left: float,
        right: float,
    ) -> bool:
        return abs(float(left) - float(right)) <= 1e-9
