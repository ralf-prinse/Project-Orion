from __future__ import annotations

from dataclasses import dataclass, field

from models.paper_position import PaperPosition


@dataclass
class PaperPortfolio:
    cash: float
    positions: dict[str, PaperPosition] = field(default_factory=dict)
    base_currency: str = "EUR"

    @property
    def positions_value(self) -> float:
        return round(
            sum(position.market_value for position in self.positions.values()),
            2,
        )

    @property
    def equity(self) -> float:
        return round(self.cash + self.positions_value, 2)
