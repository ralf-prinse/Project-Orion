from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NewsAssessment:
    symbol: str
    assessed_at: datetime
    mode: str
    status: str
    risk_level: str
    sentiment_score: float
    relevant_event_count: int
    blocking_recommended: bool
    event_ids: tuple[str, ...]
    headlines: tuple[str, ...]
    reasons: tuple[str, ...]
    provider: str
    lookback_hours: int

    @classmethod
    def disabled(
        cls,
        *,
        symbol: str,
        assessed_at: datetime,
    ) -> "NewsAssessment":
        return cls(
            symbol=symbol.strip().upper(),
            assessed_at=assessed_at,
            mode="DISABLED",
            status="DISABLED",
            risk_level="UNKNOWN",
            sentiment_score=0.0,
            relevant_event_count=0,
            blocking_recommended=False,
            event_ids=(),
            headlines=(),
            reasons=("News intelligence is disabled.",),
            provider="NONE",
            lookback_hours=0,
        )
