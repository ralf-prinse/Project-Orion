from services.scanner.quote_service import Quote


class PriceFilter:
    """
    Filtert aandelen op prijs.

    Voor swing trading willen we meestal geen extreem goedkope
    penny stocks en ook geen extreem dure aandelen.
    """

    def __init__(self, min_price: float = 2.0, max_price: float = 500.0):
        self.min_price = min_price
        self.max_price = max_price

    def apply(self, quotes: list[Quote]) -> list[Quote]:
        return [
            quote
            for quote in quotes
            if self.min_price <= quote.price <= self.max_price
        ]