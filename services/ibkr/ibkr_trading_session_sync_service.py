from __future__ import annotations

import math
import time
from collections.abc import Iterable, Mapping
from dataclasses import replace
from typing import Protocol

from models.trading_session import TradingSession
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper


class CurrentPriceProvider(Protocol):
    def get_current_price(self, symbol: str) -> float:
        ...


class IbkrTradingSessionSyncError(RuntimeError):
    """
    Raised when IBKR does not report the expected post-fill
    broker position state within the synchronization window.
    """


class IbkrTradingSessionSyncService:
    """
    Synchronizes an Orion TradingSession with the current IBKR account.

    IBKR is authoritative for:

    - available cash;
    - open positions;
    - quantities;
    - average entry prices.

    Post-fill synchronization supports two expectations:

    expected_symbols
        Backwards-compatible BUY synchronization. Poll until every
        expected symbol is present at IBKR.

    expected_position_quantities
        BUY and SELL synchronization. Poll until every supplied symbol
        has the expected broker quantity.

        An expected quantity of zero means that the position must be
        absent from the IBKR portfolio.
    """

    def __init__(
        self,
        *,
        account_service: IbkrAccountService,
        price_provider: CurrentPriceProvider,
        mapper: IbkrPortfolioMapper | None = None,
    ) -> None:
        self._account_service = account_service
        self._price_provider = price_provider
        self._mapper = mapper or IbkrPortfolioMapper()

    def synchronize(
        self,
        session: TradingSession,
        *,
        expected_symbols: Iterable[str] | None = None,
        expected_position_quantities: Mapping[str, float] | None = None,
        attempts: int = 1,
        retry_delay_seconds: float = 0.25,
    ) -> TradingSession:
        """
        Replace the local portfolio with the current IBKR portfolio.

        When expectations are supplied, IBKR positions are polled until
        the expected broker state is visible or all attempts have been
        exhausted.

        The account connection is always closed.
        """

        if attempts < 1:
            raise ValueError(
                "attempts must be at least 1."
            )

        if retry_delay_seconds < 0:
            raise ValueError(
                "retry_delay_seconds must not be negative."
            )

        normalized_expected_symbols = {
            str(symbol).strip().upper()
            for symbol in (expected_symbols or ())
            if str(symbol).strip()
        }

        normalized_expected_quantities = (
            self._normalize_expected_quantities(
                expected_position_quantities
            )
        )

        self._account_service.connect()

        try:
            account = self._account_service.read_account()

            broker_positions = ()
            reported_quantities: dict[str, float] = {}

            for attempt_index in range(attempts):
                broker_positions = tuple(
                    self._account_service.read_positions()
                )

                reported_quantities = {
                    self._comparison_symbol(
                        position.symbol
                    ): float(position.quantity)
                    for position in broker_positions
                }

                if self._expectations_satisfied(
                    reported_quantities=reported_quantities,
                    expected_symbols=normalized_expected_symbols,
                    expected_quantities=(
                        normalized_expected_quantities
                    ),
                ):
                    break

                is_last_attempt = (
                    attempt_index == attempts - 1
                )

                if (
                    not is_last_attempt
                    and retry_delay_seconds > 0
                ):
                    time.sleep(retry_delay_seconds)

            self._raise_for_unsatisfied_expectations(
                reported_quantities=reported_quantities,
                expected_symbols=normalized_expected_symbols,
                expected_quantities=(
                    normalized_expected_quantities
                ),
            )

            broker_positions = self._restore_orion_symbols(
                broker_positions=broker_positions,
                session=session,
            )

            current_prices = {
                position.symbol.strip().upper():
                self._price_provider.get_current_price(
                    position.symbol.strip().upper()
                )
                for position in broker_positions
            }

            synchronized_portfolio = self._mapper.map(
                account=account,
                positions=broker_positions,
                current_prices=current_prices,
            )

        finally:
            self._account_service.disconnect()

        synchronized_symbols = set(
            synchronized_portfolio.positions
        )

        session.portfolio = synchronized_portfolio

        session.position_states = {
            symbol: state
            for symbol, state in session.position_states.items()
            if symbol.strip().upper()
            in synchronized_symbols
        }

        session.risk_plans = {
            symbol: risk_plan
            for symbol, risk_plan in session.risk_plans.items()
            if symbol.strip().upper()
            in synchronized_symbols
        }

        return session

    def _normalize_expected_quantities(
        self,
        expected_position_quantities: (
            Mapping[str, float] | None
        ),
    ) -> dict[str, float]:
        normalized: dict[str, float] = {}

        for symbol, quantity in (
            expected_position_quantities or {}
        ).items():
            normalized_symbol = str(symbol).strip().upper()

            if not normalized_symbol:
                raise ValueError(
                    "Expected position symbol must not be empty."
                )

            try:
                normalized_quantity = float(quantity)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "Expected position quantity must be numeric."
                ) from exc

            if not math.isfinite(normalized_quantity):
                raise ValueError(
                    "Expected position quantity must be finite."
                )

            if normalized_quantity < 0:
                raise ValueError(
                    "Expected position quantity must not be negative."
                )

            normalized[normalized_symbol] = normalized_quantity

        return normalized

    def _restore_orion_symbols(
        self,
        *,
        broker_positions,
        session: TradingSession,
    ):
        """Restore Yahoo/Orion suffixes removed by IBKR contracts.

        An IBKR stock contract reports ASML while Orion deliberately uses
        ASML.AS for market data and market-session routing. A known local
        symbol is reused only when it maps unambiguously to the broker
        symbol. Unknown broker positions remain untouched and unmanaged.
        """

        known_symbols = {
            str(symbol).strip().upper()
            for symbol in (
                set(session.portfolio.positions)
                | set(session.position_states)
                | set(session.risk_plans)
            )
            if str(symbol).strip()
        }

        aliases: dict[str, list[str]] = {}
        for symbol in known_symbols:
            aliases.setdefault(
                self._comparison_symbol(symbol),
                [],
            ).append(symbol)

        restored = []
        for position in broker_positions:
            candidates = aliases.get(
                self._comparison_symbol(position.symbol),
                [],
            )
            if len(candidates) == 1:
                restored.append(
                    replace(position, symbol=candidates[0])
                )
                continue

            exchange = str(position.exchange).strip().upper()
            currency = str(position.currency).strip().upper()
            raw_symbol = str(position.symbol).strip().upper()

            if (
                not candidates
                and exchange == "AEB"
                and currency == "EUR"
                and not raw_symbol.endswith(".AS")
            ):
                restored.append(
                    replace(position, symbol=f"{raw_symbol}.AS")
                )
                continue

            restored.append(position)

        return tuple(restored)

    def _expectations_satisfied(
        self,
        *,
        reported_quantities: Mapping[str, float],
        expected_symbols: set[str],
        expected_quantities: Mapping[str, float],
    ) -> bool:
        reported_symbols = set(reported_quantities)
        expected_symbol_keys = {
            self._comparison_symbol(symbol)
            for symbol in expected_symbols
        }

        if not expected_symbol_keys.issubset(reported_symbols):
            return False

        return all(
            self._quantity_matches(
                reported_quantity=reported_quantities.get(
                    self._comparison_symbol(symbol),
                    0.0,
                ),
                expected_quantity=expected_quantity,
            )
            for symbol, expected_quantity
            in expected_quantities.items()
        )

    def _raise_for_unsatisfied_expectations(
        self,
        *,
        reported_quantities: Mapping[str, float],
        expected_symbols: set[str],
        expected_quantities: Mapping[str, float],
    ) -> None:
        missing_symbols = {
            symbol
            for symbol in expected_symbols
            if self._comparison_symbol(symbol)
            not in reported_quantities
        }

        if missing_symbols:
            raise IbkrTradingSessionSyncError(
                "IBKR did not report the expected "
                "post-fill position(s): "
                + ", ".join(sorted(missing_symbols))
            )

        quantity_mismatches: list[str] = []

        for symbol, expected_quantity in (
            expected_quantities.items()
        ):
            reported_quantity = reported_quantities.get(
                self._comparison_symbol(symbol),
                0.0,
            )

            if not self._quantity_matches(
                reported_quantity=reported_quantity,
                expected_quantity=expected_quantity,
            ):
                quantity_mismatches.append(
                    f"{symbol}: expected "
                    f"{expected_quantity:g}, reported "
                    f"{reported_quantity:g}"
                )

        if quantity_mismatches:
            raise IbkrTradingSessionSyncError(
                "IBKR did not report the expected "
                "post-fill position quantity: "
                + "; ".join(quantity_mismatches)
            )

    def _comparison_symbol(self, symbol: str) -> str:
        normalized = str(symbol).strip().upper()

        if normalized.endswith(".AS"):
            return normalized[:-3]

        return normalized

    def _quantity_matches(
        self,
        *,
        reported_quantity: float,
        expected_quantity: float,
    ) -> bool:
        return math.isclose(
            float(reported_quantity),
            float(expected_quantity),
            rel_tol=0.0,
            abs_tol=1e-9,
        )
