from ui.foundation.models import GuiNavigationItem, GuiPage


class NavigationRegistry:
    """
    Deterministic navigation registry for the Orion desktop GUI.

    The registry defines presentation structure only. It does not know anything
    about market data, analysis, signals, decisions, portfolio state or risk.
    """

    def __init__(self, items: list[GuiNavigationItem] | None = None):
        self._items = items or self._default_items()

    def get_items(self) -> list[GuiNavigationItem]:
        return sorted(self._items, key=lambda item: item.order)

    def contains_page(self, page: GuiPage) -> bool:
        return any(item.page == page for item in self._items)

    def get_default_page(self) -> GuiPage:
        items = self.get_items()
        if not items:
            return GuiPage.DASHBOARD
        return items[0].page

    @staticmethod
    def _default_items() -> list[GuiNavigationItem]:
        return [
            GuiNavigationItem(GuiPage.DASHBOARD, "Dashboard", 10),
            GuiNavigationItem(GuiPage.SCANNER, "Scanner", 20),
            GuiNavigationItem(GuiPage.PORTFOLIO, "Portfolio", 30),
            GuiNavigationItem(GuiPage.BACKTESTING, "Backtesting", 40),
            GuiNavigationItem(GuiPage.PAPER_TRADING, "Paper Trading", 50),
            GuiNavigationItem(GuiPage.TRADE_PLANNER, "Trade Planner", 60),
            GuiNavigationItem(GuiPage.PERFORMANCE, "Performance", 70),
            GuiNavigationItem(GuiPage.SETTINGS, "Settings", 80),
        ]
