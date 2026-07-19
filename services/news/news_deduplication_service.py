from __future__ import annotations

from models.news_event import NewsEvent


class NewsDeduplicationService:
    def deduplicate(
        self,
        events: tuple[NewsEvent, ...],
    ) -> tuple[NewsEvent, ...]:
        seen_ids: set[str] = set()
        seen_headlines: set[tuple[str, str]] = set()
        unique: list[NewsEvent] = []

        for event in sorted(events, key=lambda item: item.published_at):
            headline_key = (
                event.provider,
                event.normalized_headline,
            )
            if (
                event.event_id in seen_ids
                or headline_key in seen_headlines
            ):
                continue
            seen_ids.add(event.event_id)
            seen_headlines.add(headline_key)
            unique.append(event)

        return tuple(unique)
