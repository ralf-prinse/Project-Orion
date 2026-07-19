from __future__ import annotations

from datetime import UTC, datetime, timedelta

from models.news_assessment import NewsAssessment
from services.news.news_assessment_service import NewsAssessmentService
from services.news.news_deduplication_service import NewsDeduplicationService
from services.news.news_normalizer import NewsNormalizer
from services.news.provider import NewsProvider


class NewsIntelligenceService:
    """Collects and records news in shadow mode without changing trades."""

    def __init__(
        self,
        *,
        provider: NewsProvider,
        event_repository=None,
        assessment_repository=None,
        normalizer: NewsNormalizer | None = None,
        deduplication_service: NewsDeduplicationService | None = None,
        assessment_service: NewsAssessmentService | None = None,
        lookback_hours: int = 24,
        max_articles_per_symbol: int = 10,
        clock=None,
    ) -> None:
        if lookback_hours < 1:
            raise ValueError("lookback_hours must be at least 1.")
        if max_articles_per_symbol < 1:
            raise ValueError(
                "max_articles_per_symbol must be at least 1."
            )
        self.provider = provider
        self.event_repository = event_repository
        self.assessment_repository = assessment_repository
        self.normalizer = normalizer or NewsNormalizer()
        self.deduplication_service = (
            deduplication_service or NewsDeduplicationService()
        )
        self.assessment_service = (
            assessment_service or NewsAssessmentService()
        )
        self.lookback_hours = int(lookback_hours)
        self.max_articles_per_symbol = int(max_articles_per_symbol)
        self.clock = clock or (lambda: datetime.now(UTC))

    def assess_symbols(
        self,
        symbols,
    ) -> dict[str, NewsAssessment]:
        normalized_symbols = tuple(
            dict.fromkeys(
                str(symbol).strip().upper()
                for symbol in symbols
                if str(symbol).strip()
            )
        )
        if not normalized_symbols:
            return {}

        assessed_at = self._as_utc(self.clock())
        since = assessed_at - timedelta(hours=self.lookback_hours)
        try:
            raw_items = self.provider.fetch_recent(
                symbols=normalized_symbols,
                since=since,
                max_articles_per_symbol=self.max_articles_per_symbol,
            )
            normalized_events = []
            for item in raw_items:
                try:
                    event = self.normalizer.normalize(
                        item,
                        received_at=assessed_at,
                    )
                    if since <= event.published_at <= assessed_at:
                        normalized_events.append(event)
                except ValueError:
                    continue
            events = self.deduplication_service.deduplicate(
                tuple(normalized_events)
            )
            for event in events:
                if self.event_repository is not None:
                    self.event_repository.append_unique(event)
            assessments = {
                symbol: self.assessment_service.assess(
                    symbol=symbol,
                    events=events,
                    provider=self.provider.name,
                    lookback_hours=self.lookback_hours,
                    assessed_at=assessed_at,
                    mode="SHADOW",
                )
                for symbol in normalized_symbols
            }
        except Exception as exc:
            safe_reason = (
                "News intelligence unavailable in SHADOW mode: "
                f"{type(exc).__name__}: {exc}"
            )
            assessments = {
                symbol: self.assessment_service.unavailable(
                    symbol=symbol,
                    provider=self.provider.name,
                    lookback_hours=self.lookback_hours,
                    reason=safe_reason,
                    assessed_at=assessed_at,
                )
                for symbol in normalized_symbols
            }

        if self.assessment_repository is not None:
            for assessment in assessments.values():
                self.assessment_repository.append(assessment)
        return assessments

    def _as_utc(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
