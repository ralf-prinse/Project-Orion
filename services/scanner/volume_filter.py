from services.scanner.quote_service import Quote


class VolumeFilter:
    """
    Filtert aandelen op minimaal dagvolume.
    """

    def __init__(self, min_volume: int = 500_000):
        self.min_volume = min_volume

    def apply(self, quotes: list[Quote]) -> list[Quote]:
        return [
            quote
            for quote in quotes
            if quote.volume >= self.min_volume
        ]