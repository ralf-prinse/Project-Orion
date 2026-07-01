from dataclasses import dataclass

from ui.foundation.models import GuiPage


@dataclass(frozen=True)
class OrionIcons:
    """
    Lightweight icon mapping for navigation labels.

    The first version deliberately uses Unicode symbols instead of external icon
    dependencies. A future icon provider can replace this map without changing
    presenters or navigation models.
    """

    dashboard: str = "◈"
    universe: str = "◎"
    market_data: str = "◆"
    historical_data: str = "◷"
    decisions: str = "✓"
    analysis: str = "▤"
    indicators: str = "▧"
    signals: str = "↗"
    scanner: str = "⌕"
    portfolio: str = "▣"
    risk: str = "⚠"
    backtesting: str = "⟲"
    paper_trading: str = "◌"
    trade_planner: str = "⌁"
    performance: str = "▰"
    settings: str = "⚙"

    def for_page(self, page: GuiPage) -> str:
        return getattr(self, page.value, "•")


ORION_ICONS = OrionIcons()
