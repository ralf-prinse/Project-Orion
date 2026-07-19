from __future__ import annotations

from datetime import datetime
from typing import Protocol

from models.news_event import RawNewsItem


class NewsProvider(Protocol):
    @property
    def name(self) -> str:
        ...

    def fetch_recent(
        self,
        *,
        symbols: tuple[str, ...],
        since: datetime,
        max_articles_per_symbol: int,
    ) -> tuple[RawNewsItem, ...]:
        ...
