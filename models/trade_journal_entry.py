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

    trade_id: str = ""

    strategy_name: str = "ORION_CANONICAL"

    risk_allowed: bool | None = None

    proposed_risk_ratio: float | None = None

    total_portfolio_risk: float | None = None

    drawdown: float | None = None

    cash_reserve_after_trade: float | None = None

    position_exposure: float | None = None

    risk_reasons: tuple[str, ...] = ()

    risk_warnings: tuple[str, ...] = ()

    estimated_trading_costs: float = 0.0

    estimated_net_profit_loss: float = 0.0

    profit_calculation_currency: str = "EUR"

    news_mode: str = "DISABLED"
    news_status: str = "NOT_EVALUATED"
    news_risk_level: str = "UNKNOWN"
    news_sentiment_score: float = 0.0
    news_blocking_recommended: bool = False
    news_event_ids: tuple[str, ...] = ()
    news_headlines: tuple[str, ...] = ()
    news_reasons: tuple[str, ...] = ()
    news_provider: str = "NONE"

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
