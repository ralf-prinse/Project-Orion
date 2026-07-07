from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TradeJournalEntry:
    """
    Immutable journal entry for one completed trading decision.

    This model is the canonical historical record used by ORION
    to analyse its own behaviour over time.
    """

    timestamp: datetime

    symbol: str

    action: str

    decision: str

    confidence: float

    score: float

    entry_price: float

    exit_price: float | None

    quantity: int

    invested_amount: float

    realized_profit_loss: float

    unrealized_profit_loss: float

    expected_risk: float

    regime: str

    volatility: str

    ai_summary: str

    recommendation_reason: str

    cycle_number: int

    session_id: str

    @property
    def total_return_percent(self) -> float:
        if self.invested_amount <= 0:
            return 0.0

        return round(
            (self.realized_profit_loss / self.invested_amount) * 100,
            2,
        )

    @property
    def was_profitable(self) -> bool:
        return self.realized_profit_loss > 0