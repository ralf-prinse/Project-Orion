from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RawNewsItem:
    provider: str
    article_id: str
    headline: str
    published_at: datetime
    symbols: tuple[str, ...]
    url: str | None = None


@dataclass(frozen=True)
class NewsEvent:
    event_id: str
    provider: str
    article_id: str
    headline: str
    normalized_headline: str
    published_at: datetime
    received_at: datetime
    symbols: tuple[str, ...]
    category: str
    sentiment: float
    severity: str
    reliability: float
    url: str | None = None
