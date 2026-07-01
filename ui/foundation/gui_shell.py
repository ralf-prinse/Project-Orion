from services.ai.models import AIExplanationResult
from services.analysis.models import AnalysisResult, IndicatorResult
from services.backtesting.models import BacktestResult
from services.decisions.models import DecisionResult
from services.signals.models import SignalResult
from services.market_data.base_provider import MarketDataProviderStats, MarketQuote
from services.market_data.historical_provider import HistoricalProviderStats
from ui.foundation.analysis_presenter import AnalysisPresenter
from ui.foundation.indicator_presenter import IndicatorPresenter
from ui.foundation.historical_data_presenter import HistoricalDataPresenter
from ui.foundation.market_data_presenter import MarketDataPresenter
from ui.foundation.backtesting_presenter import BacktestingPresenter
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.dashboard_presenter import DashboardPresenter
from ui.foundation.decision_presenter import DecisionPresenter
from ui.foundation.explanation_presenter import ExplanationPresenter
from services.performance.models import PerformanceResult
from services.paper_trading.models import PaperTradingResult
from services.portfolio.models import PortfolioResult, PortfolioState
from services.planner.models import TradePlanResult
from typing import Any
from ui.foundation.models import GuiApplicationConfig, GuiPage, GuiSection, GuiShellState
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter
from ui.foundation.paper_trading_presenter import PaperTradingPresenter
from ui.foundation.portfolio_presenter import PortfolioPresenter
from ui.foundation.scanner_presenter import ScannerPresenter
from ui.foundation.signal_presenter import SignalPresenter
from ui.foundation.trade_plan_presenter import TradePlanPresenter


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
        dashboard_composer: DashboardComposer | None = None,
    ):
        self.config = config or GuiApplicationConfig()
        self.navigation_registry = navigation_registry or NavigationRegistry()
        self.dashboard_presenter = dashboard_presenter or DashboardPresenter()
        self.explanation_presenter = explanation_presenter or ExplanationPresenter()
        self.performance_dashboard_presenter = (
            performance_dashboard_presenter or PerformanceDashboardPresenter()
        )
        self.backtesting_presenter = backtesting_presenter or BacktestingPresenter()
        self.paper_trading_presenter = paper_trading_presenter or PaperTradingPresenter()
        self.trade_plan_presenter = trade_plan_presenter or TradePlanPresenter()
        self.scanner_presenter = scanner_presenter or ScannerPresenter()
        self.portfolio_presenter = portfolio_presenter or PortfolioPresenter()
        self.decision_presenter = decision_presenter or DecisionPresenter()
        self.signal_presenter = signal_presenter or SignalPresenter()
        self.analysis_presenter = analysis_presenter or AnalysisPresenter()
        self.indicator_presenter = indicator_presenter or IndicatorPresenter()
        self.market_data_presenter = market_data_presenter or MarketDataPresenter()
        self.historical_data_presenter = historical_data_presenter or HistoricalDataPresenter()
        self.dashboard_composer = dashboard_composer or DashboardComposer(
            performance_presenter=self.performance_dashboard_presenter,
            backtesting_presenter=self.backtesting_presenter,
            paper_trading_presenter=self.paper_trading_presenter,
            trade_plan_presenter=self.trade_plan_presenter,
            explanation_presenter=self.explanation_presenter,
            scanner_presenter=self.scanner_presenter,
            portfolio_presenter=self.portfolio_presenter,
            decision_presenter=self.decision_presenter,
            signal_presenter=self.signal_presenter,
            analysis_presenter=self.analysis_presenter,
            indicator_presenter=self.indicator_presenter,
            market_data_presenter=self.market_data_presenter,
            historical_data_presenter=self.historical_data_presenter,
        )
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


    def build_backtesting_dashboard(self, backtest_result: BacktestResult) -> GuiShellState:
        self.state.sections = self.backtesting_presenter.create_sections(backtest_result)
        self.state.current_page = GuiPage.BACKTESTING
        self.state.status_message = "Backtesting dashboard updated"
        return self.state

    def build_paper_trading_dashboard(self, paper_trading_result: PaperTradingResult) -> GuiShellState:
        self.state.sections = self.paper_trading_presenter.create_sections(paper_trading_result)
        self.state.current_page = GuiPage.PAPER_TRADING
        self.state.status_message = "Paper trading dashboard updated"
        return self.state

    def build_trade_plan_dashboard(self, trade_plan_result: TradePlanResult) -> GuiShellState:
        self.state.sections = self.trade_plan_presenter.create_sections(trade_plan_result)
        self.state.current_page = GuiPage.TRADE_PLANNER
        self.state.status_message = "Trade plan dashboard updated"
        return self.state


    def build_market_data_dashboard(
        self,
        quotes: list[MarketQuote],
        stats: MarketDataProviderStats | None = None,
    ) -> GuiShellState:
        self.state.sections = self.market_data_presenter.create_sections(quotes, stats)
        self.state.current_page = GuiPage.MARKET_DATA
        self.state.status_message = "Market data dashboard updated"
        return self.state



    def build_historical_data_dashboard(
        self,
        histories: dict[str, Any],
        stats: HistoricalProviderStats | None = None,
    ) -> GuiShellState:
        self.state.sections = self.historical_data_presenter.create_sections(histories, stats)
        self.state.current_page = GuiPage.HISTORICAL_DATA
        self.state.status_message = "Historical data dashboard updated"
        return self.state

    def build_decision_dashboard(self, decision_result: DecisionResult) -> GuiShellState:
        self.state.sections = self.decision_presenter.create_sections(decision_result)
        self.state.current_page = GuiPage.DECISIONS
        self.state.status_message = "Decision dashboard updated"
        return self.state


    def build_analysis_dashboard(self, analysis_result: AnalysisResult) -> GuiShellState:
        self.state.sections = self.analysis_presenter.create_sections(analysis_result)
        self.state.current_page = GuiPage.ANALYSIS
        self.state.status_message = "Analysis dashboard updated"
        return self.state

    def build_indicator_dashboard(self, indicator_result: IndicatorResult) -> GuiShellState:
        self.state.sections = self.indicator_presenter.create_sections(indicator_result)
        self.state.current_page = GuiPage.INDICATORS
        self.state.status_message = "Indicator dashboard updated"
        return self.state

    def build_signal_dashboard(self, signal_result: SignalResult) -> GuiShellState:
        self.state.sections = self.signal_presenter.create_sections(signal_result)
        self.state.current_page = GuiPage.SIGNALS
        self.state.status_message = "Signal dashboard updated"
        return self.state

    def build_scanner_dashboard(self, scanner_result: Any) -> GuiShellState:
        self.state.sections = self.scanner_presenter.create_sections(scanner_result)
        self.state.current_page = GuiPage.SCANNER
        self.state.status_message = "Scanner dashboard updated"
        return self.state

    def build_portfolio_dashboard(
        self,
        portfolio_state: PortfolioState,
        portfolio_result: PortfolioResult | None = None,
    ) -> GuiShellState:
        self.state.sections = self.portfolio_presenter.create_sections(
            portfolio_state=portfolio_state,
            portfolio_result=portfolio_result,
        )
        self.state.current_page = GuiPage.PORTFOLIO
        self.state.status_message = "Portfolio dashboard updated"
        return self.state

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
    ) -> GuiShellState:
        self.state.sections = self.dashboard_composer.compose(
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
        )
        self.state.current_page = GuiPage.DASHBOARD
        self.state.status_message = "Unified dashboard updated"
        return self.state

    def _resolve_initial_page(self, preferred_page: GuiPage) -> GuiPage:
        if self.navigation_registry.contains_page(preferred_page):
            return preferred_page
        return self.navigation_registry.get_default_page()
