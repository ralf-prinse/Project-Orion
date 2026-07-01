from services.ai.models import AIExplanationResult
from ui.foundation.dashboard_presenter import DashboardPresenter
from ui.foundation.explanation_presenter import ExplanationPresenter
from services.performance.models import PerformanceResult
from services.paper_trading.models import PaperTradingResult
from ui.foundation.models import GuiApplicationConfig, GuiPage, GuiSection, GuiShellState
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter
from ui.foundation.paper_trading_presenter import PaperTradingPresenter


class GuiShell:
    """
    Toolkit-independent GUI shell foundation.

    PySide6 windows can use this class as a deterministic source of navigation,
    page state and dashboard sections. The shell contains presentation state only
    and deliberately avoids trading logic.
    """

    def __init__(
        self,
        config: GuiApplicationConfig | None = None,
        navigation_registry: NavigationRegistry | None = None,
        dashboard_presenter: DashboardPresenter | None = None,
        explanation_presenter: ExplanationPresenter | None = None,
        performance_dashboard_presenter: PerformanceDashboardPresenter | None = None,
        paper_trading_presenter: PaperTradingPresenter | None = None,
    ):
        self.config = config or GuiApplicationConfig()
        self.navigation_registry = navigation_registry or NavigationRegistry()
        self.dashboard_presenter = dashboard_presenter or DashboardPresenter()
        self.explanation_presenter = explanation_presenter or ExplanationPresenter()
        self.performance_dashboard_presenter = (
            performance_dashboard_presenter or PerformanceDashboardPresenter()
        )
        self.paper_trading_presenter = paper_trading_presenter or PaperTradingPresenter()
        self.state = GuiShellState(
            current_page=self._resolve_initial_page(self.config.default_page),
            navigation_items=self.navigation_registry.get_items(),
        )

    def navigate_to(self, page: GuiPage) -> GuiShellState:
        if not self.navigation_registry.contains_page(page):
            raise ValueError(f"Unknown GUI page: {page.value}")
        self.state.current_page = page
        self.state.status_message = f"Current page: {page.value}"
        return self.state

    def set_sections(self, sections: list[GuiSection]) -> GuiShellState:
        self.state.sections = sections
        return self.state

    def set_status_message(self, message: str) -> GuiShellState:
        self.state.status_message = message.strip() or "Ready"
        return self.state

    def build_dashboard(self, **kwargs) -> GuiShellState:
        self.state.sections = self.dashboard_presenter.create_overview_sections(**kwargs)
        self.state.current_page = GuiPage.DASHBOARD
        self.state.status_message = "Dashboard updated"
        return self.state

    def build_explanation(self, explanation_result: AIExplanationResult) -> GuiShellState:
        self.state.sections = self.explanation_presenter.create_sections(explanation_result)
        self.state.current_page = GuiPage.DASHBOARD
        self.state.status_message = "Explanation updated"
        return self.state


    def build_performance_dashboard(self, performance_result: PerformanceResult) -> GuiShellState:
        self.state.sections = self.performance_dashboard_presenter.create_sections(performance_result)
        self.state.current_page = GuiPage.PERFORMANCE
        self.state.status_message = "Performance dashboard updated"
        return self.state

    def build_paper_trading_dashboard(self, paper_trading_result: PaperTradingResult) -> GuiShellState:
        self.state.sections = self.paper_trading_presenter.create_sections(paper_trading_result)
        self.state.current_page = GuiPage.PAPER_TRADING
        self.state.status_message = "Paper trading dashboard updated"
        return self.state

    def _resolve_initial_page(self, preferred_page: GuiPage) -> GuiPage:
        if self.navigation_registry.contains_page(preferred_page):
            return preferred_page
        return self.navigation_registry.get_default_page()
