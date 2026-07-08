from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from models.paper_portfolio import PaperPortfolio


class PaperPortfolioRepository(ABC):
    """
    Abstract repository for PaperPortfolio persistence.

    Trading services must depend only on this contract.

    Concrete implementations may use:

    - JSON
    - SQLite
    - PostgreSQL
    - Cloud storage

    without requiring changes to the trading domain.
    """

    @abstractmethod
    def exists(self) -> bool:
        """
        Returns True when a persisted portfolio exists.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self) -> PaperPortfolio:
        """
        Loads the complete portfolio.

        Raises:
            FileNotFoundError
                When no persisted portfolio exists.
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        portfolio: PaperPortfolio,
    ) -> None:
        """
        Persists the complete portfolio.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        """
        Removes the persisted portfolio.
        """
        raise NotImplementedError