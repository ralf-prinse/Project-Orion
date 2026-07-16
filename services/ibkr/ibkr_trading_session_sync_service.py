from __future__ import annotations

import time
from collections.abc import Iterable
from typing import Protocol

from models.trading_session import TradingSession
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper


class CurrentPriceProvider(Protocol):
    def get_current_price(self, symbol: str) -> float:
        ...


class IbkrTradingSessionSyncError(RuntimeError):
    """
    Raised when IBKR does not report an expected broker position
    within the configured synchronization window.
    """


class IbkrTradingSessionSyncService:
    """
    Synchronizes an Orion TradingSession with the current IBKR account.

    IBKR is treated as the source of truth for:

    - available cash;
    - open positions;
    - quantities;
    - average entry prices.

    For post-fill synchronization, expected_symbols can be supplied.
    The service then polls IBKR until those symbols appear or until
    the configured number of attempts is exhausted.
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
        attempts: int = 1,
        retry_delay_seconds: float = 0.25,
    ) -> TradingSession:
        """
        Replace the local portfolio with the current IBKR portfolio.

        When expected_symbols is supplied, IBKR positions are polled
        until all expected symbols are visible.

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

        self._account_service.connect()

        try:
            account = self._account_service.read_account()

            broker_positions = ()
            reported_symbols: set[str] = set()

            for attempt_index in range(attempts):
                broker_positions = (
                    self._account_service.read_positions()
                )

                reported_symbols = {
                    position.symbol.strip().upper()
                    for position in broker_positions
                }

                expected_positions_visible = (
                    normalized_expected_symbols
                    .issubset(reported_symbols)
                )

                if expected_positions_visible:
                    break

                is_last_attempt = (
                    attempt_index == attempts - 1
                )

                if (
                    not is_last_attempt
                    and retry_delay_seconds > 0
                ):
                    time.sleep(retry_delay_seconds)

            missing_symbols = (
                normalized_expected_symbols
                - reported_symbols
            )

            if missing_symbols:
                raise IbkrTradingSessionSyncError(
                    "IBKR did not report the expected "
                    "post-fill position(s): "
                    + ", ".join(sorted(missing_symbols))
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