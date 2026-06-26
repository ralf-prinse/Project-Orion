from services.scanner.quote_service import Quote


class LiquidityFilter:
    """
    Filtert aandelen op dollar volume.

    Dollar volume = prijs * volume.

    Dit voorkomt aandelen die wel volume hebben,
    maar nauwelijks echte handelswaarde.
    """

    def __init__(self, min_dollar_volume: float = 10_000_000):
        self.min_dollar_volume = min_dollar_volume

    def apply(self, quotes: list[Quote]) -> list[Quote]:
        return [
            quote
            for quote in quotes
            if quote.price * quote.volume >= self.min_dollar_volume
        ]