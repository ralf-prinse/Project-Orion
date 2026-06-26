from dataclasses import dataclass


@dataclass
class Portfolio:
    cash: float
    currency: str = "EUR"
    max_position_percentage: float = 0.35

    def max_position_value(self) -> float:
        return self.cash * self.max_position_percentage