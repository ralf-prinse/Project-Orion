from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperPosition:
    symbol: str
    quantity: int
    entry_price: float
    current_price: float

    @property
    def market_value(self) -> float:
        return round(self.quantity * self.current_price, 2)

    @property
    def cost_basis(self) -> float:
        return round(self.quantity * self.entry_price, 2)

    @property
    def unrealized_profit_loss(self) -> float:
        return round(self.market_value - self.cost_basis, 2)