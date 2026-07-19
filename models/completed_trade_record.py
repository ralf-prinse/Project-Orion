from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CompletedTradeRecord:
    """Canonical, immutable memory of one fully closed trade."""

    trade_id: str
    symbol: str
    strategy_name: str
    opened_at: datetime
    closed_at: datetime
    quantity: int
    entry_price: float
    exit_price: float
    invested_amount: float
    gross_profit_loss: float
    estimated_trading_costs: float
    estimated_net_profit_loss: float
    profit_calculation_currency: str
    holding_seconds: float
    entry_decision: str
    entry_confidence: float
    entry_score: float
    entry_regime: str
    entry_volatility: str
    entry_summary: str
    entry_reason: str
    exit_decision: str
    exit_reason: str
    adopted_position: bool
    original_entry_rationale_available: bool
    entry_news_status: str
    entry_news_risk_level: str
    entry_news_sentiment_score: float
    entry_news_event_ids: tuple[str, ...]
    exit_news_status: str
    exit_news_risk_level: str
    exit_news_sentiment_score: float
    exit_news_event_ids: tuple[str, ...]

    @property
    def was_profitable_after_estimated_costs(self) -> bool:
        return self.estimated_net_profit_loss > 0
