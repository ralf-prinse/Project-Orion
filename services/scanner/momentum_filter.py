from services.scanner.quote_service import Quote


class MomentumFilter:
    """
    Selecteert aandelen met de beste korte-termijn momentum.

    Sprint 5.1:
    - Gebruikt voorlopig dezelfde proxy als RelativeStrengthFilter.
    - Wordt later vervangen door echte momentum-analyse.
    """

    def apply(self, quotes: list[Quote], limit: int = 500) -> list[Quote]:
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