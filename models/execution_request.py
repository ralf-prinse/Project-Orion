from __future__ import annotations

from dataclasses import dataclass

from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class ExecutionRequest:
    symbol: str
    action: str
    entry_price: float
    quantity: int
    risk_plan: RiskPlan
    confidence: float
    strategy: str = "DEFAULT"
    source: str = "TradingPipeline"
    currency: str = "EUR"
    fx_rate_to_base: float = 1.0
    trade_id: str = ""
    execution_urgency: str = "NORMAL"
