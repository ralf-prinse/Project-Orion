from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from models.trading_session import TradingSession


class TradingSessionRepository(ABC):
    """
    Abstract repository for complete TradingSession persistence.

    The persisted session contains:
    - PaperPortfolio
    - PositionState objects
    - RiskPlan objects
    - session metadata

    Trading services depend only on this contract.
    Concrete implementations may use JSON, SQLite or another
    persistence mechanism without changing the trading domain.
    """

    @abstractmethod
    def exists(self) -> bool:
        """
        Return True when a persisted trading session exists.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self) -> TradingSession:
        """
        Load the complete trading session.

        Raises:
            FileNotFoundError:
                When no persisted trading session exists.
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        session: TradingSession,
    ) -> None:
        """
        Persist the complete trading session.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        """
        Remove the persisted trading session.
        """
        raise NotImplementedError