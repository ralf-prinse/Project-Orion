from services.scanner.quote_service import Quote


class RelativeStrengthFilter:
    """
    Rangschikt aandelen op relatieve sterkte.

    Sprint 5.1:
    - Sorteert voorlopig op change_percent als simpele proxy.
    """

    def apply(self, quotes: list[Quote], limit: int = 1000) -> list[Quote]:
        scored_quotes = [
            quote
            for quote in quotes
            if quote.change_percent is not None
        ]

        scored_quotes.sort(
            key=lambda quote: quote.change_percent,
            reverse=True,
        )

        return scored_quotes[:limit]