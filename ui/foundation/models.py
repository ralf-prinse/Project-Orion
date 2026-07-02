from dataclasses import dataclass, field
from enum import Enum


class GuiPage(str, Enum):
    """
    Stable page identifiers for the professional Orion desktop shell.

    These identifiers are intentionally independent from any specific GUI
    toolkit. PySide6 widgets can consume them later without introducing trading
    logic into the presentation layer.
    """

    DASHBOARD = "dashboard"
    UNIVERSE = "universe"
    MARKET_DATA = "market_data"
    HISTORICAL_DATA = "historical_data"
    DECISIONS = "decisions"
    ANALYSIS = "analysis"
    INDICATORS = "indicators"
    SIGNALS = "signals"
    SCANNER = "scanner"
    PORTFOLIO = "portfolio"
    HISTORY = "history"
    RISK = "risk"
    BACKTESTING = "backtesting"
    PAPER_TRADING = "paper_trading"
    TRADE_PLANNER = "trade_planner"
    PERFORMANCE = "performance"
    SETTINGS = "settings"


@dataclass(frozen=True)
class GuiNavigationItem:
    """
    One deterministic item in the application navigation.
    """

    page: GuiPage
    label: str
    order: int
    enabled: bool = True


@dataclass(frozen=True)
class GuiMetric:
    """
    Presentation-safe metric for cards, dashboards and reports.
    """

    label: str
    value: str
    helper_text: str = ""


@dataclass(frozen=True)
class GuiMetricCard:
    """
    Presentation-safe KPI card.
    """

    title: str
    value: str
    subtitle: str = ""
    trend: str = ""


@dataclass(frozen=True)
class GuiSection:
    """
    Logical GUI section containing display-only metrics.
    """

    title: str
    metrics: list[GuiMetric] = field(default_factory=list)
    description: str = ""


@dataclass(frozen=True)
class GuiWorkspace:
    """
    Complete presentation model for one workspace.

    A workspace can contain multiple presentation component types while keeping
    the public workspace API stable.
    """

    cards: list[GuiMetricCard] = field(default_factory=list)
    sections: list[GuiSection] = field(default_factory=list)


@dataclass(frozen=True)
class GuiApplicationConfig:
    """
    Static configuration for the desktop shell.
    """

    application_name: str = "Project Orion"
    subtitle: str = "Deterministic Swing Trading Platform"
    default_page: GuiPage = GuiPage.DASHBOARD
    version: str = "v1.0.8-alpha"


@dataclass
class GuiShellState:
    """
    Runtime state of the GUI shell.
    """

    current_page: GuiPage = GuiPage.DASHBOARD
    navigation_items: list[GuiNavigationItem] = field(default_factory=list)
    sections: list[GuiSection] = field(default_factory=list)
    status_message: str = "Ready"

    def enabled_navigation_items(self) -> list[GuiNavigationItem]:
        return [item for item in self.navigation_items if item.enabled]