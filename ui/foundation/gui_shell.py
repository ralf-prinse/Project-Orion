from typing import Any

from services.ai.models import AIExplanationResult
from services.analysis.models import AnalysisResult, IndicatorResult
from services.backtesting.models import BacktestResult
from services.decisions.models import DecisionResult
from services.market_data.base_provider import MarketDataProviderStats, MarketQuote
from services.market_data.historical_provider import HistoricalProviderStats
from services.paper_trading.models import PaperTradingResult
from services.performance.models import PerformanceResult
from services.planner.models import TradePlanResult
from services.portfolio.models import PortfolioResult, PortfolioState
from services.signals.models import SignalResult
from ui.foundation.analysis_presenter import AnalysisPresenter
from ui.foundation.backtesting_presenter import BacktestingPresenter
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.dashboard_presenter import DashboardPresenter
from ui.foundation.dashboard_router import DashboardRouter
from ui.foundation.decision_presenter import DecisionPresenter
from ui.foundation.explanation_presenter import ExplanationPresenter
from ui.foundation.historical_data_presenter import HistoricalDataPresenter
from ui.foundation.indicator_presenter import IndicatorPresenter
from ui.foundation.market_data_presenter import MarketDataPresenter
from ui.foundation.models import GuiApplicationConfig, GuiPage, GuiSection, GuiShellState
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.paper_trading_presenter import PaperTradingPresenter
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter
from ui.foundation.portfolio_presenter import PortfolioPresenter
from ui.foundation.scanner_presenter import ScannerPresenter
from ui.foundation.signal_presenter import SignalPresenter
from ui.foundation.trade_plan_presenter import TradePlanPresenter
from ui.foundation.universe_presenter import UniversePresenter


class GuiShell:
    """
    Toolkit-independent GUI shell foundation.

    PySide6 windows can use this class as a deterministic source of navigation,
    page state and dashboard sections. The shell contains presentation state only
    and deliberately avoids trading logic.

    Dashboard section construction is delegated to DashboardRouter so the shell
    remains focused on page state, navigation state and status messages.
    """

    def __init__(
        self,
        config: GuiApplicationConfig | None = None,
        navigation_registry: NavigationRegistry | None = None,
        dashboard_presenter: DashboardPresenter | None = None,
        explanation_presenter: ExplanationPresenter | None = None,
        performance_dashboard_presenter: PerformanceDashboardPresenter | None = None,
        backtesting_presenter: BacktestingPresenter | None = None,
        paper_trading_presenter: PaperTradingPresenter | None = None,
        trade_plan_presenter: TradePlanPresenter | None = None,
        scanner_presenter: ScannerPresenter | None = None,
        portfolio_presenter: PortfolioPresenter | None = None,
        decision_presenter: DecisionPresenter | None = None,
        signal_presenter: SignalPresenter | None = None,
        analysis_presenter: AnalysisPresenter | None = None,
        indicator_presenter: IndicatorPresenter | None = None,
        market_data_presenter: MarketDataPresenter | None = None,
        historical_data_presenter: HistoricalDataPresenter | None = None,
        universe_presenter: UniversePresenter | None = None,
        dashboard_composer: DashboardComposer | None = None,
        dashboard_router: DashboardRouter | None = None,
    ):
        self.config = config or GuiApplicationConfig()
        self.navigation_registry = navigation_registry or NavigationRegistry()

        self.dashboard_router = dashboard_router or DashboardRouter(
            dashboard_presenter=dashboard_presenter,
            explanation_presenter=explanation_presenter,
            performance_presenter=performance_dashboard_presenter,
            backtesting_presenter=backtesting_presenter,
            paper_trading_presenter=paper_trading_presenter,
            trade_plan_presenter=trade_plan_presenter,
            scanner_presenter=scanner_presenter,
            portfolio_presenter=portfolio_presenter,
            decision_presenter=decision_presenter,
            signal_presenter=signal_presenter,
            analysis_presenter=analysis_presenter,
            indicator_presenter=indicator_presenter,
            market_data_presenter=market_data_presenter,
            historical_data_presenter=historical_data_presenter,
            universe_presenter=universe_presenter,
            dashboard_composer=dashboard_composer,
        )

        self.dashboard_presenter = self.dashboard_router.dashboard_presenter
        self.explanation_presenter = self.dashboard_router.explanation_presenter
        self.performance_dashboard_presenter = self.dashboard_router.performance_presenter
        self.backtesting_presenter = self.dashboard_router.backtesting_presenter
        self.paper_trading_presenter = self.dashboard_router.paper_trading_presenter
        self.trade_plan_presenter = self.dashboard_router.trade_plan_presenter
        self.scanner_presenter = self.dashboard_router.scanner_presenter
        self.portfolio_presenter = self.dashboard_router.portfolio_presenter
        self.decision_presenter = self.dashboard_router.decision_presenter
        self.signal_presenter = self.dashboard_router.signal_presenter
        self.analysis_presenter = self.dashboard_router.analysis_presenter
        self.indicator_presenter = self.dashboard_router.indicator_presenter
        self.market_data_presenter = self.dashboard_router.market_data_presenter
        self.historical_data_presenter = self.dashboard_router.historical_data_presenter
        self.universe_presenter = self.dashboard_router.universe_presenter
        self.dashboard_composer = self.dashboard_router.dashboard_composer

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
        return self._update_dashboard(
            page=GuiPage.DASHBOARD,
            sections=self.dashboard_router.build_overview(**kwargs),
            status_message="Dashboard updated",
        )

    def build_explanation(self, explanation_result: AIExplanationResult) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.DASHBOARD,
            sections=self.dashboard_router.build_explanation(explanation_result),
            status_message="Explanation updated",
        )

    def build_performance_dashboard(
        self,
        performance_result: PerformanceResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.PERFORMANCE,
            sections=self.dashboard_router.build_performance(performance_result),
            status_message="Performance dashboard updated",
        )

    def build_backtesting_dashboard(
        self,
        backtest_result: BacktestResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.BACKTESTING,
            sections=self.dashboard_router.build_backtesting(backtest_result),
            status_message="Backtesting dashboard updated",
        )

    def build_paper_trading_dashboard(
        self,
        paper_trading_result: PaperTradingResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.PAPER_TRADING,
            sections=self.dashboard_router.build_paper_trading(paper_trading_result),
            status_message="Paper trading dashboard updated",
        )

    def build_trade_plan_dashboard(
        self,
        trade_plan_result: TradePlanResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.TRADE_PLANNER,
            sections=self.dashboard_router.build_trade_plan(trade_plan_result),
            status_message="Trade plan dashboard updated",
        )

    def build_universe_dashboard(
        self,
        symbols: list[str],
        update_stats: dict[str, Any] | None = None,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.UNIVERSE,
            sections=self.dashboard_router.build_universe(symbols, update_stats),
            status_message="Universe dashboard updated",
        )

    def build_market_data_dashboard(
        self,
        quotes: list[MarketQuote],
        stats: MarketDataProviderStats | None = None,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.MARKET_DATA,
            sections=self.dashboard_router.build_market_data(quotes, stats),
            status_message="Market data dashboard updated",
        )

    def build_historical_data_dashboard(
        self,
        histories: dict[str, Any],
        stats: HistoricalProviderStats | None = None,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.HISTORICAL_DATA,
            sections=self.dashboard_router.build_historical_data(histories, stats),
            status_message="Historical data dashboard updated",
        )

    def build_decision_dashboard(
        self,
        decision_result: DecisionResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.DECISIONS,
            sections=self.dashboard_router.build_decision(decision_result),
            status_message="Decision dashboard updated",
        )

    def build_analysis_dashboard(
        self,
        analysis_result: AnalysisResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.ANALYSIS,
            sections=self.dashboard_router.build_analysis(analysis_result),
            status_message="Analysis dashboard updated",
        )

    def build_indicator_dashboard(
        self,
        indicator_result: IndicatorResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.INDICATORS,
            sections=self.dashboard_router.build_indicator(indicator_result),
            status_message="Indicator dashboard updated",
        )

    def build_signal_dashboard(
        self,
        signal_result: SignalResult,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.SIGNALS,
            sections=self.dashboard_router.build_signal(signal_result),
            status_message="Signal dashboard updated",
        )

    def build_scanner_dashboard(self, scanner_result: Any) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.SCANNER,
            sections=self.dashboard_router.build_scanner(scanner_result),
            status_message="Scanner dashboard updated",
        )

    def build_portfolio_dashboard(
        self,
        portfolio_state: PortfolioState,
        portfolio_result: PortfolioResult | None = None,
    ) -> GuiShellState:
        sections = self.portfolio_presenter.create_sections(
            portfolio_state=portfolio_state,
            portfolio_result=portfolio_result,
        )

        return self._update_dashboard(
            page=GuiPage.PORTFOLIO,
            sections=sections,
            status_message="Portfolio dashboard updated",
        )

    def build_unified_dashboard(
        self,
        performance_result: PerformanceResult | None = None,
        backtest_result: BacktestResult | None = None,
        paper_trading_result: PaperTradingResult | None = None,
        trade_plan_result: TradePlanResult | None = None,
        explanation_result: AIExplanationResult | None = None,
        scanner_result: Any | None = None,
        portfolio_state: PortfolioState | None = None,
        portfolio_result: PortfolioResult | None = None,
        decision_result: DecisionResult | None = None,
        signal_result: SignalResult | None = None,
        analysis_result: AnalysisResult | None = None,
        indicator_result: IndicatorResult | None = None,
        market_quotes: list[MarketQuote] | None = None,
        quote_stats: MarketDataProviderStats | None = None,
        historical_data: dict[str, Any] | None = None,
        historical_stats: HistoricalProviderStats | None = None,
        universe_symbols: list[str] | None = None,
        universe_update_stats: dict[str, Any] | None = None,
    ) -> GuiShellState:
        return self._update_dashboard(
            page=GuiPage.DASHBOARD,
            sections=self.dashboard_router.build_composed_dashboard(
                performance_result=performance_result,
                backtest_result=backtest_result,
                paper_trading_result=paper_trading_result,
                trade_plan_result=trade_plan_result,
                explanation_result=explanation_result,
                scanner_result=scanner_result,
                portfolio_state=portfolio_state,
                portfolio_result=portfolio_result,
                decision_result=decision_result,
                signal_result=signal_result,
                analysis_result=analysis_result,
                indicator_result=indicator_result,
                market_quotes=market_quotes,
                quote_stats=quote_stats,
                historical_data=historical_data,
                historical_stats=historical_stats,
                universe_symbols=universe_symbols,
                universe_update_stats=universe_update_stats,
            ),
            status_message="Unified dashboard updated",
        )

    def _update_dashboard(
        self,
        page: GuiPage,
        sections: list[GuiSection],
        status_message: str,
    ) -> GuiShellState:
        self.state.sections = sections
        self.state.current_page = page
        self.state.status_message = status_message
        return self.state

    def _resolve_initial_page(self, preferred_page: GuiPage) -> GuiPage:
        if self.navigation_registry.contains_page(preferred_page):
            return preferred_page
        return self.navigation_registry.get_default_page()