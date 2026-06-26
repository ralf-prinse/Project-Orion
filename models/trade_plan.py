from dataclasses import dataclass


@dataclass
class TradePlan:
    action: str
    symbol: str
    quantity: int
    estimated_price: float
    estimated_value: float
    currency: str