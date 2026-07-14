from __future__ import annotations

from collections.abc import Mapping

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from models.paper_portfolio import PaperPortfolio
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_portfolio_mapper import (
    IbkrPortfolioMapper,
)


class IbkrPortfolioService:
    """
    Facade that converts the current IBKR Paper account into an Orion
    PaperPortfolio.

    Responsibilities:

    - read broker account
    - read broker positions
    - invoke the mapper

    Responsibilities intentionally NOT included:

    - market data
    - caching
    - execution
    - trading session
    - lifecycle state
    """

    def __init__(
        self,
        *,
        account_service: IbkrAccountService,
        mapper: IbkrPortfolioMapper | None = None,
    ) -> None:
        self._account_service = account_service
        self._mapper = mapper or IbkrPortfolioMapper()

    def read_account(self) -> BrokerAccount:
        return self._account_service.read_account()

    def read_positions(self) -> list[BrokerPosition]:
        return self._account_service.read_positions()

    def read_portfolio(
        self,
        *,
        current_prices: Mapping[str, float],
    ) -> PaperPortfolio:
        account = self.read_account()

        positions = self.read_positions()

        return self._mapper.map(
            account=account,
            positions=positions,
            current_prices=current_prices,
        )