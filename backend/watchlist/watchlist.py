from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WatchlistItem:
    """
    Presentation-independent watchlist item.

    This model represents a single symbol that Orion continuously monitors.

    It intentionally contains no trading logic.
    It only describes what should be scanned.
    """

    symbol: str

    enabled: bool = True

    priority: int = 100

    exchange: str = ""

    sector: str = ""

    industry: str = ""

    tags: tuple[str, ...] = field(default_factory=tuple)

    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Watchlist:
    """
    Immutable watchlist definition.

    The LiveMarketScanner receives a Watchlist and determines
    which symbols should be analysed.

    The scanner never hardcodes symbols.
    """

    name: str

    items: tuple[WatchlistItem, ...] = field(default_factory=tuple)

    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def enabled_items(self) -> tuple[WatchlistItem, ...]:
        """
        Returns only enabled symbols.
        """
        return tuple(item for item in self.items if item.enabled)

    @property
    def symbols(self) -> tuple[str, ...]:
        """
        Returns the enabled ticker symbols.
        """
        return tuple(item.symbol for item in self.enabled_items)