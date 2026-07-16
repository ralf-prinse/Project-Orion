from __future__ import annotations

from typing import Protocol

from models.trading_session import TradingSession
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper


class CurrentPriceProvider(Protocol):
    def get_current_price(self, symbol: str) -> float:
        ...


class IbkrTradingSessionSyncService:
    """
    Synchronizes an Orion TradingSession with the current IBKR Paper account.

    IBKR is treated as the source of truth for:

    - available cash;
    - open positions;
    - quantities;
    - average entry prices.

    Existing risk plans and position states are preserved only for symbols
    that are still present in the broker portfolio.
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
    ) -> TradingSession:
        """
        Replace the local session portfolio with the current IBKR portfolio.

        The account connection is always closed, including when reading,
        pricing or mapping fails.
        """

        self._account_service.connect()

        try:
            account = self._account_service.read_account()
            broker_positions = self._account_service.read_positions()

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
            if symbol.strip().upper() in synchronized_symbols
        }

        session.risk_plans = {
            symbol: risk_plan
            for symbol, risk_plan in session.risk_plans.items()
            if symbol.strip().upper() in synchronized_symbols
        }

        return session