from dataclasses import dataclass, field
from enum import Enum


class GuiPage(str, Enum):
    """
    Stable page identifiers for the professional Orion desktop shell.
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
    Generic reusable KPI card used throughout Orion.

    This model is presentation-only and intentionally contains no
    business logic.
    """

    title: str
    value: str

    subtitle: str = ""
    trend: str = ""

    icon: str = ""
    accent_color: str = ""
    status: str = "default"
    size: str = "normal"

    column_span: int = 1


@dataclass(frozen=True)
class GuiSection:
    """
    Logical GUI section containing display-only metrics.
    """

    title: str
    metrics: list[GuiMetric] = field(default_factory=list)
    description: str = ""


@dataclass(frozen=True)
class GuiChartPoint:
    """
    One presentation-safe data point for a chart.
    """

    label: str
    value: float


@dataclass(frozen=True)
class GuiChart:
    """
    Presentation-safe chart model.
    """

    title: str
    points: list[GuiChartPoint] = field(default_factory=list)
    chart_type: str = "line"
    description: str = ""
    unit: str = ""


@dataclass(frozen=True)
class GuiWorkspace:
    """
    Complete presentation model for one workspace.
    """

    cards: list[GuiMetricCard] = field(default_factory=list)
    charts: list[GuiChart] = field(default_factory=list)
    sections: list[GuiSection] = field(default_factory=list)


@dataclass(frozen=True)
class GuiApplicationConfig:
    """
    Static configuration for the desktop shell.
    """

    application_name: str = "Project Orion"
    subtitle: str = "Deterministic Swing Trading Platform"
    default_page: GuiPage = GuiPage.DASHBOARD
    version: str = "v1.2.0-alpha"


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
        return [
            item
            for item in self.navigation_items
            if item.enabled
        ]