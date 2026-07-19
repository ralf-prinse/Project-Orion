from __future__ import annotations

from datetime import UTC, datetime

from models.news_assessment import NewsAssessment
from models.news_event import NewsEvent


class NewsAssessmentService:
    """Builds an informational assessment; never changes an order."""

    RISK_RANK = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    def assess(
        self,
        *,
        symbol: str,
        events: tuple[NewsEvent, ...],
        provider: str,
        lookback_hours: int,
        assessed_at: datetime | None = None,
        mode: str = "SHADOW",
    ) -> NewsAssessment:
        normalized_symbol = symbol.strip().upper()
        now = self._as_utc(assessed_at or datetime.now(UTC))
        relevant = tuple(
            event
            for event in events
            if normalized_symbol in event.symbols
        )

        if not relevant:
            return NewsAssessment(
                symbol=normalized_symbol,
                assessed_at=now,
                mode=mode,
                status="NO_NEWS",
                risk_level="LOW",
                sentiment_score=0.0,
                relevant_event_count=0,
                blocking_recommended=False,
                event_ids=(),
                headlines=(),
                reasons=("No relevant news returned in the lookback window.",),
                provider=provider,
                lookback_hours=lookback_hours,
            )

        risk_level = max(
            (event.severity for event in relevant),
            key=lambda level: self.RISK_RANK.get(level, 0),
        )
        weighted_sentiment = self._weighted_sentiment(
            events=relevant,
            now=now,
            lookback_hours=lookback_hours,
        )
        blocking_recommended = (
            risk_level in {"HIGH", "CRITICAL"}
            and any(event.sentiment < 0 for event in relevant)
        )
        reasons = [
            f"Assessed {len(relevant)} unique news event(s).",
            f"Highest observed severity is {risk_level}.",
            f"Freshness-weighted sentiment is {weighted_sentiment:.3f}.",
        ]
        if blocking_recommended:
            reasons.append(
                "Shadow gate would recommend blocking a new BUY."
            )
        reasons.append("SHADOW mode did not alter trading behavior.")

        newest_first = tuple(
            sorted(relevant, key=lambda event: event.published_at, reverse=True)
        )
        return NewsAssessment(
            symbol=normalized_symbol,
            assessed_at=now,
            mode=mode,
            status="AVAILABLE",
            risk_level=risk_level,
            sentiment_score=weighted_sentiment,
            relevant_event_count=len(relevant),
            blocking_recommended=blocking_recommended,
            event_ids=tuple(event.event_id for event in newest_first),
            headlines=tuple(event.headline for event in newest_first[:5]),
            reasons=tuple(reasons),
            provider=provider,
            lookback_hours=lookback_hours,
        )

    def unavailable(
        self,
        *,
        symbol: str,
        provider: str,
        lookback_hours: int,
        reason: str,
        assessed_at: datetime | None = None,
    ) -> NewsAssessment:
        return NewsAssessment(
            symbol=symbol.strip().upper(),
            assessed_at=self._as_utc(assessed_at or datetime.now(UTC)),
            mode="SHADOW",
            status="UNAVAILABLE",
            risk_level="UNKNOWN",
            sentiment_score=0.0,
            relevant_event_count=0,
            blocking_recommended=False,
            event_ids=(),
            headlines=(),
            reasons=(reason, "Trading behavior was not altered."),
            provider=provider,
            lookback_hours=lookback_hours,
        )

    def _weighted_sentiment(
        self,
        *,
        events: tuple[NewsEvent, ...],
        now: datetime,
        lookback_hours: int,
    ) -> float:
        weighted_total = 0.0
        total_weight = 0.0
        window = max(1.0, float(lookback_hours))
        for event in events:
            age_hours = max(
                0.0,
                (now - self._as_utc(event.published_at)).total_seconds()
                / 3600.0,
            )
            freshness = max(0.05, 1.0 - (age_hours / window))
            weight = freshness * event.reliability
            weighted_total += event.sentiment * weight
            total_weight += weight
        if total_weight <= 0:
            return 0.0
        return round(weighted_total / total_weight, 4)

    def _as_utc(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
