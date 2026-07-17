from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperPosition:
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    currency: str = "EUR"
    fx_rate_to_base: float = 1.0

    @property
    def market_value(self) -> float:
        return round(
            self.quantity * self.current_price * self.fx_rate_to_base,
            2,
        )

    @property
    def cost_basis(self) -> float:
        return round(
            self.quantity * self.entry_price * self.fx_rate_to_base,
            2,
        )

    @property
    def unrealized_profit_loss(self) -> float:
        return round(self.market_value - self.cost_basis, 2)
