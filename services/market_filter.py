from dataclasses import dataclass


@dataclass
class FilteredSymbol:
    symbol: str
    price: float
    accepted: bool
    reason: str = ""


class MarketFilter:
    """
    Filtert aandelen vóórdat Orion zware analyse uitvoert.

    Doel:
    - geen penny stocks
    - geen extreem dure aandelen bij klein portfolio
    - alleen aandelen die binnen jouw handelsstijl passen
    """

    def __init__(
        self,
        min_price: float = 5.0,
        max_price: float = 500.0,
    ):
        self.min_price = min_price
        self.max_price = max_price

    def accept(self, symbol: str, price: float) -> FilteredSymbol:
        if price <= 0:
            return FilteredSymbol(
                symbol=symbol,
                price=price,
                accepted=False,
                reason="Geen geldige koers.",
            )

        if price < self.min_price:
            return FilteredSymbol(
                symbol=symbol,
                price=price,
                accepted=False,
                reason="Koers te laag.",
            )

        if price > self.max_price:
            return FilteredSymbol(
                symbol=symbol,
                price=price,
                accepted=False,
                reason="Koers te hoog voor huidige portfolio-instelling.",
            )

        return FilteredSymbol(
            symbol=symbol,
            price=price,
            accepted=True,
            reason="Aandeel voldoet aan basisfilter.",
        )