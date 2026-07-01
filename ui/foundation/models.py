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
    SCANNER = "scanner"
    PORTFOLIO = "portfolio"
    BACKTESTING = "backtesting"
    PAPER_TRADING = "paper_trading"
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

    The GUI layer receives already calculated values from deterministic engines.
    It may format and group them, but it must not calculate trading decisions.
    """

    label: str
    value: str
    helper_text: str = ""


@dataclass(frozen=True)
class GuiSection:
    """
    Logical GUI section containing display-only metrics.
    """

    title: str
    metrics: list[GuiMetric] = field(default_factory=list)
    description: str = ""


@dataclass(frozen=True)
class GuiApplicationConfig:
    """
    Static configuration for the desktop shell.
    """

    application_name: str = "Project Orion"
    subtitle: str = "Deterministic Swing Trading Platform"
    default_page: GuiPage = GuiPage.DASHBOARD
    version: str = "v0.9.4-alpha"


@dataclass
class GuiShellState:
    """
    Runtime state of the GUI shell.

    This state is intentionally small. Engine state, portfolio state and trade
    state stay inside their own layers and are only projected into view models.
    """

    current_page: GuiPage = GuiPage.DASHBOARD
    navigation_items: list[GuiNavigationItem] = field(default_factory=list)
    sections: list[GuiSection] = field(default_factory=list)
    status_message: str = "Ready"

    def enabled_navigation_items(self) -> list[GuiNavigationItem]:
        return [item for item in self.navigation_items if item.enabled]
