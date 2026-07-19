from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import UTC, datetime

from models.news_event import NewsEvent, RawNewsItem


class NewsNormalizer:
    """Normalizes provider news without making trading decisions."""

    CRITICAL_NEGATIVE = (
        "bankruptcy",
        "insolvency",
        "accounting fraud",
        "trading halt",
        "sanctioned",
        "files for chapter 11",
        "faillissement",
        "insolvenz",
        "bilanzbetrug",
        "handel ausgesetzt",
    )
    HIGH_NEGATIVE = (
        "profit warning",
        "cuts guidance",
        "lowers guidance",
        "recall",
        "investigation",
        "data breach",
        "misses estimates",
        "downgrade",
        "winstwaarschuwing",
        "verlaagt prognose",
        "gegevenslek",
        "gewinnwarnung",
        "senkt prognose",
        "datenleck",
    )
    POSITIVE = (
        "beats estimates",
        "raises guidance",
        "approval",
        "wins contract",
        "upgrade",
        "record revenue",
        "verhoogt prognose",
        "goedkeuring",
        "wint opdracht",
        "erhoht prognose",
        "zulassung",
        "gewinnt auftrag",
    )

    def normalize(
        self,
        item: RawNewsItem,
        *,
        received_at: datetime | None = None,
    ) -> NewsEvent:
        headline = " ".join(str(item.headline).split()).strip()
        if not headline:
            raise ValueError("News headline must not be empty.")

        provider = str(item.provider).strip().upper()
        if not provider:
            raise ValueError("News provider must not be empty.")

        published_at = self._as_utc(item.published_at)
        normalized_headline = self._normalized_text(headline)
        symbols = tuple(
            dict.fromkeys(
                str(symbol).strip().upper()
                for symbol in item.symbols
                if str(symbol).strip()
            )
        )
        if not symbols:
            raise ValueError("News item must contain at least one symbol.")

        category, sentiment, severity = self._classify(
            normalized_headline
        )
        article_id = str(item.article_id).strip()
        identity = (
            f"{provider}:{article_id}"
            if article_id
            else f"{provider}:{normalized_headline}:{published_at.isoformat()}"
        )
        event_id = hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()

        return NewsEvent(
            event_id=event_id,
            provider=provider,
            article_id=article_id,
            headline=headline,
            normalized_headline=normalized_headline,
            published_at=published_at,
            received_at=self._as_utc(received_at or datetime.now(UTC)),
            symbols=symbols,
            category=category,
            sentiment=sentiment,
            severity=severity,
            reliability=1.0,
            url=item.url,
        )

    def _classify(self, text: str) -> tuple[str, float, str]:
        if any(term in text for term in self.CRITICAL_NEGATIVE):
            return "COMPANY_RISK", -1.0, "CRITICAL"
        if any(term in text for term in self.HIGH_NEGATIVE):
            return "COMPANY_RISK", -0.75, "HIGH"
        if any(term in text for term in self.POSITIVE):
            return "COMPANY_UPDATE", 0.65, "LOW"
        if any(term in text for term in ("earnings", "revenue", "guidance")):
            return "EARNINGS", 0.0, "MEDIUM"
        if any(
            term in text
            for term in (
                "fed", "ecb", "interest rate", "inflation",
                "rente", "zinssatz",
            )
        ):
            return "MACRO", 0.0, "MEDIUM"
        if any(
            term in text
            for term in (
                "war", "tariff", "sanction", "oorlog", "heffing",
                "krieg", "zoll", "sanktion",
            )
        ):
            return "GEOPOLITICAL", -0.4, "HIGH"
        return "GENERAL", 0.0, "LOW"

    def _normalized_text(self, value: str) -> str:
        lowered = "".join(
            character
            for character in unicodedata.normalize("NFKD", value.casefold())
            if not unicodedata.combining(character)
        )
        return re.sub(r"[^a-z0-9]+", " ", lowered).strip()

    def _as_utc(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
