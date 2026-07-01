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
from ui.foundation.decision_presenter import DecisionPresenter
from ui.foundation.explanation_presenter import ExplanationPresenter
from ui.foundation.historical_data_presenter import HistoricalDataPresenter
from ui.foundation.indicator_presenter import IndicatorPresenter
from ui.foundation.market_data_presenter import MarketDataPresenter
from ui.foundation.models import GuiSection
from ui.foundation.paper_trading_presenter import PaperTradingPresenter
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter
from ui.foundation.portfolio_presenter import PortfolioPresenter
from ui.foundation.scanner_presenter import ScannerPresenter
from ui.foundation.signal_presenter import SignalPresenter
from ui.foundation.trade_plan_presenter import TradePlanPresenter
from ui.foundation.universe_presenter import UniversePresenter


class DashboardRouter:
    """
    Routes deterministic result objects to presentation-only dashboard sections.

    The router centralizes dashboard composition decisions without importing Qt,
    creating widgets, calling services or performing trading calculations.
    """

    def __init__(
        self,
        dashboard_presenter: DashboardPresenter | None = None,
        explanation_presenter: ExplanationPresenter | None = None,
        performance_presenter: PerformanceDashboardPresenter | None = None,
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
    ):
        self.dashboard_presenter = dashboard_presenter or DashboardPresenter()
        self.explanation_presenter = explanation_presenter or ExplanationPresenter()
        self.performance_presenter = performance_presenter or PerformanceDashboardPresenter()
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
        self.universe_presenter = universe_presenter or UniversePresenter()
        self.dashboard_composer = dashboard_composer or DashboardComposer(
            performance_presenter=self.performance_presenter,
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
            universe_presenter=self.universe_presenter,
        )

    def build_overview(
        self,
        performance_result: PerformanceResult | None = None,
        total_open_positions: int = 0,
        total_watchlist_items: int = 0,
    ) -> list[GuiSection]:
        return self.dashboard_presenter.create_overview_sections(
            performance_result=performance_result,
            total_open_positions=total_open_positions,
            total_watchlist_items=total_watchlist_items,
        )

    def build_explanation(self, explanation_result: AIExplanationResult) -> list[GuiSection]:
        return self.explanation_presenter.create_sections(explanation_result)

    def build_performance(self, performance_result: PerformanceResult) -> list[GuiSection]:
        return self.performance_presenter.create_sections(performance_result)

    def build_backtesting(self, backtest_result: BacktestResult) -> list[GuiSection]:
        return self.backtesting_presenter.create_sections(backtest_result)

    def build_paper_trading(
        self,
        paper_trading_result: PaperTradingResult,
    ) -> list[GuiSection]:
        return self.paper_trading_presenter.create_sections(paper_trading_result)

    def build_trade_plan(self, trade_plan_result: TradePlanResult) -> list[GuiSection]:
        return self.trade_plan_presenter.create_sections(trade_plan_result)

    def build_universe(
        self,
        symbols: list[str],
        update_stats: dict[str, Any] | None = None,
    ) -> list[GuiSection]:
        return self.universe_presenter.create_sections(symbols, update_stats)

    def build_market_data(
        self,
        quotes: list[MarketQuote],
        stats: MarketDataProviderStats | None = None,
    ) -> list[GuiSection]:
        return self.market_data_presenter.create_sections(quotes, stats)

    def build_historical_data(
        self,
        histories: dict[str, Any],
        stats: HistoricalProviderStats | None = None,
    ) -> list[GuiSection]:
        return self.historical_data_presenter.create_sections(histories, stats)

    def build_decision(self, decision_result: DecisionResult) -> list[GuiSection]:
        return self.decision_presenter.create_sections(decision_result)

    def build_analysis(self, analysis_result: AnalysisResult) -> list[GuiSection]:
        return self.analysis_presenter.create_sections(analysis_result)

    def build_indicator(self, indicator_result: IndicatorResult) -> list[GuiSection]:
        return self.indicator_presenter.create_sections(indicator_result)

    def build_signal(self, signal_result: SignalResult) -> list[GuiSection]:
        return self.signal_presenter.create_sections(signal_result)

    def build_scanner(self, scanner_result: Any) -> list[GuiSection]:
        return self.scanner_presenter.create_sections(scanner_result)

    def build_portfolio_state(self, portfolio_state: PortfolioState) -> list[GuiSection]:
        return self.portfolio_presenter.create_state_sections(portfolio_state)

    def build_portfolio_result(self, portfolio_result: PortfolioResult) -> list[GuiSection]:
        return self.portfolio_presenter.create_result_sections(portfolio_result)

    def build_composed_dashboard(
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
    ) -> list[GuiSection]:
        return self.dashboard_composer.compose(
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
        )