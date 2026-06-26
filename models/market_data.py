from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketData:
    symbol: str
    name: str
    exchange: str
    currency: str

    current_price: float
    open_price: float
    high_price: float
    low_price: float
    previous_close: float
    volume: int

    timestamp: datetime