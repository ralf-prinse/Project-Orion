from services.ai.models import AIExplanationResult
from services.paper_trading.models import PaperTradingResult
from services.performance.models import PerformanceResult
from services.planner.models import TradePlanResult
from ui.foundation.explanation_presenter import ExplanationPresenter
from ui.foundation.models import GuiMetric, GuiSection
from ui.foundation.paper_trading_presenter import PaperTradingPresenter
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter
from ui.foundation.trade_plan_presenter import TradePlanPresenter


class DashboardComposer:
    """
    Composes multiple deterministic Orion result views into one dashboard.

    The composer is presentation-only. It delegates all formatting to existing
    presenters and never calculates performance, paper-trading state, trade
    plans, explanations, signals, decisions or risk outcomes.
    """

    def __init__(
        self,
        performance_presenter: PerformanceDashboardPresenter | None = None,
        paper_trading_presenter: PaperTradingPresenter | None = None,
        trade_plan_presenter: TradePlanPresenter | None = None,
        explanation_presenter: ExplanationPresenter | None = None,
    ):
        self.performance_presenter = performance_presenter or PerformanceDashboardPresenter()
        self.paper_trading_presenter = paper_trading_presenter or PaperTradingPresenter()
        self.trade_plan_presenter = trade_plan_presenter or TradePlanPresenter()
        self.explanation_presenter = explanation_presenter or ExplanationPresenter()

    def compose(
        self,
        performance_result: PerformanceResult | None = None,
        paper_trading_result: PaperTradingResult | None = None,
        trade_plan_result: TradePlanResult | None = None,
        explanation_result: AIExplanationResult | None = None,
    ) -> list[GuiSection]:
        sections: list[GuiSection] = [
            self._create_summary_section(
                performance_result=performance_result,
                paper_trading_result=paper_trading_result,
                trade_plan_result=trade_plan_result,
                explanation_result=explanation_result,
            )
        ]

        if performance_result is not None:
            sections.extend(self.performance_presenter.create_sections(performance_result))

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
        paper_trading_result: PaperTradingResult | None,
        trade_plan_result: TradePlanResult | None,
        explanation_result: AIExplanationResult | None,
    ) -> GuiSection:
        active_modules = []

        if performance_result is not None:
            active_modules.append("Performance")
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
