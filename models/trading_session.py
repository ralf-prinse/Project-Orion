from __future__ import annotations

from dataclasses import dataclass, field

from models.paper_portfolio import PaperPortfolio
from models.position_state import PositionState


@dataclass
class TradingSession:
    """
    Runtime paper-trading session.

    No trading decisions.
    No broker logic.
    No AI.
    """

    name: str
    portfolio: PaperPortfolio
    position_states: dict[str, PositionState] = field(default_factory=dict)
    status: str = "ACTIVE"

    @property
    def cash(self) -> float:
        return self.portfolio.cash

    @property
    def equity(self) -> float:
        return self.portfolio.equity

    @property
    def open_positions(self) -> int:
        return len(self.portfolio.positions)