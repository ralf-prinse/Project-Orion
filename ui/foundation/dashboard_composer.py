from services.ai.models import AIExplanationResult
from services.analysis.models import AnalysisResult, IndicatorResult
from services.decisions.models import DecisionResult
from services.backtesting.models import BacktestResult
from services.paper_trading.models import PaperTradingResult
from services.portfolio.models import PortfolioResult, PortfolioState
from services.performance.models import PerformanceResult
from services.planner.models import TradePlanResult
from services.signals.models import SignalResult
from services.market_data.base_provider import MarketDataProviderStats, MarketQuote
from typing import Any
from ui.foundation.analysis_presenter import AnalysisPresenter
from ui.foundation.indicator_presenter import IndicatorPresenter
from ui.foundation.market_data_presenter import MarketDataPresenter
from ui.foundation.backtesting_presenter import BacktestingPresenter
from ui.foundation.decision_presenter import DecisionPresenter
from ui.foundation.explanation_presenter import ExplanationPresenter
from ui.foundation.models import GuiMetric, GuiSection
from ui.foundation.paper_trading_presenter import PaperTradingPresenter
from ui.foundation.portfolio_presenter import PortfolioPresenter
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter
from ui.foundation.scanner_presenter import ScannerPresenter
from ui.foundation.signal_presenter import SignalPresenter
from ui.foundation.trade_plan_presenter import TradePlanPresenter


class DashboardComposer:
    """
    Composes multiple deterministic Orion result views into one dashboard.

    The composer is presentation-only. It delegates all formatting to existing
    presenters and never calculates performance, backtesting, paper-trading
    state, trade plans, explanations, signals, decisions or risk outcomes.
    """

    def __init__(
        self,
        performance_presenter: PerformanceDashboardPresenter | None = None,
        backtesting_presenter: BacktestingPresenter | None = None,
        paper_trading_presenter: PaperTradingPresenter | None = None,
        trade_plan_presenter: TradePlanPresenter | None = None,
        explanation_presenter: ExplanationPresenter | None = None,
        scanner_presenter: ScannerPresenter | None = None,
        portfolio_presenter: PortfolioPresenter | None = None,
        decision_presenter: DecisionPresenter | None = None,
        signal_presenter: SignalPresenter | None = None,
        analysis_presenter: AnalysisPresenter | None = None,
        indicator_presenter: IndicatorPresenter | None = None,
        market_data_presenter: MarketDataPresenter | None = None,
    ):
        self.performance_presenter = performance_presenter or PerformanceDashboardPresenter()
        self.backtesting_presenter = backtesting_presenter or BacktestingPresenter()
        self.paper_trading_presenter = paper_trading_presenter or PaperTradingPresenter()
        self.trade_plan_presenter = trade_plan_presenter or TradePlanPresenter()
        self.explanation_presenter = explanation_presenter or ExplanationPresenter()
        self.scanner_presenter = scanner_presenter or ScannerPresenter()
        self.portfolio_presenter = portfolio_presenter or PortfolioPresenter()
        self.decision_presenter = decision_presenter or DecisionPresenter()
        self.signal_presenter = signal_presenter or SignalPresenter()
        self.analysis_presenter = analysis_presenter or AnalysisPresenter()
        self.indicator_presenter = indicator_presenter or IndicatorPresenter()
        self.market_data_presenter = market_data_presenter or MarketDataPresenter()

    def compose(
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
    ) -> list[GuiSection]:
        sections: list[GuiSection] = [
            self._create_summary_section(
                performance_result=performance_result,
                backtest_result=backtest_result,
                paper_trading_result=paper_trading_result,
                trade_plan_result=trade_plan_result,
                explanation_result=explanation_result,
                scanner_result=scanner_result,
                portfolio_state=portfolio_state,
                decision_result=decision_result,
                signal_result=signal_result,
                analysis_result=analysis_result,
                indicator_result=indicator_result,
                market_quotes=market_quotes,
            )
        ]

        if market_quotes is not None:
            sections.extend(self.market_data_presenter.create_sections(market_quotes, quote_stats))

        if decision_result is not None:
            sections.extend(self.decision_presenter.create_sections(decision_result))

        if analysis_result is not None:
            sections.extend(self.analysis_presenter.create_sections(analysis_result))

        if indicator_result is not None:
            sections.extend(self.indicator_presenter.create_sections(indicator_result))

        if signal_result is not None:
            sections.extend(self.signal_presenter.create_sections(signal_result))

        if scanner_result is not None:
            sections.extend(self.scanner_presenter.create_sections(scanner_result))

        if portfolio_state is not None:
            sections.extend(
                self.portfolio_presenter.create_sections(
                    portfolio_state=portfolio_state,
                    portfolio_result=portfolio_result,
                )
            )

        if performance_result is not None:
            sections.extend(self.performance_presenter.create_sections(performance_result))

        if backtest_result is not None:
            sections.extend(self.backtesting_presenter.create_sections(backtest_result))

        if paper_trading_result is not None:
            sections.extend(self.paper_trading_presenter.create_sections(paper_trading_result))

        if trade_plan_result is not None:
            sections.extend(self.trade_plan_presenter.create_sections(trade_plan_result))

        if explanation_result is not None:
            sections.extend(self.explanation_presenter.create_sections(explanation_result))

        return sections

    def _create_summary_section(
        self,
        performance_result: PerformanceResult | None,
        backtest_result: BacktestResult | None,
        paper_trading_result: PaperTradingResult | None,
        trade_plan_result: TradePlanResult | None,
        explanation_result: AIExplanationResult | None,
        scanner_result: Any | None,
        portfolio_state: PortfolioState | None,
        decision_result: DecisionResult | None,
        signal_result: SignalResult | None,
        analysis_result: AnalysisResult | None,
        indicator_result: IndicatorResult | None,
        market_quotes: list[MarketQuote] | None,
    ) -> GuiSection:
        active_modules = []

        if market_quotes is not None:
            active_modules.append("Market Data")
        if decision_result is not None:
            active_modules.append("Decisions")
        if analysis_result is not None:
            active_modules.append("Analysis")
        if indicator_result is not None:
            active_modules.append("Indicators")
        if signal_result is not None:
            active_modules.append("Signals")
        if scanner_result is not None:
            active_modules.append("Scanner")
        if portfolio_state is not None:
            active_modules.append("Portfolio")
        if performance_result is not None:
            active_modules.append("Performance")
        if backtest_result is not None:
            active_modules.append("Backtesting")
        if paper_trading_result is not None:
            active_modules.append("Paper Trading")
        if trade_plan_result is not None:
            active_modules.append("Trade Planner")
        if explanation_result is not None:
            active_modules.append("AI Explanation")

        modules_value = ", ".join(active_modules) if active_modules else "None"

        return GuiSection(
            title="Unified Dashboard Summary",
            description="Composed presentation view of deterministic Orion outputs.",
            metrics=[
                GuiMetric("Active Modules", modules_value),
                GuiMetric("Module Count", str(len(active_modules))),
                GuiMetric("Presentation Only", "Yes"),
            ],
        )
