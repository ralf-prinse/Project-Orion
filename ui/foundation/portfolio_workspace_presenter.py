from services.portfolio.analytics_service import PortfolioAnalyticsService
from services.portfolio.models import PortfolioState
from ui.foundation.models import GuiWorkspace
from ui.foundation.portfolio_analytics_presenter import (
    PortfolioAnalyticsPresenter,
)
from ui.foundation.portfolio_chart_presenter import PortfolioChartPresenter
from ui.foundation.portfolio_metric_card_presenter import (
    PortfolioMetricCardPresenter,
)
from ui.foundation.portfolio_presenter import PortfolioPresenter
from ui.foundation.equity_curve_presenter import EquityCurvePresenter


class PortfolioWorkspacePresenter:
    """
    Composes the complete Portfolio workspace presentation model.

    Responsibilities:
    - KPI cards
    - Charts (including Equity Curve)
    - Sections
    """

    def __init__(
        self,
        portfolio_presenter: PortfolioPresenter | None = None,
        analytics_service: PortfolioAnalyticsService | None = None,
        analytics_presenter: PortfolioAnalyticsPresenter | None = None,
        metric_card_presenter: PortfolioMetricCardPresenter | None = None,
        chart_presenter: PortfolioChartPresenter | None = None,
        equity_curve_presenter: EquityCurvePresenter | None = None,
    ):
        self.portfolio_presenter = portfolio_presenter or PortfolioPresenter()
        self.analytics_service = analytics_service or PortfolioAnalyticsService()
        self.analytics_presenter = (
            analytics_presenter or PortfolioAnalyticsPresenter()
        )
        self.metric_card_presenter = (
            metric_card_presenter or PortfolioMetricCardPresenter()
        )
        self.chart_presenter = (
            chart_presenter or PortfolioChartPresenter()
        )

        # NEW: Equity curve presenter (direct integration)
        self.equity_curve_presenter = (
            equity_curve_presenter or EquityCurvePresenter()
        )

    def create_workspace(
        self,
        portfolio_state: PortfolioState,
    ) -> GuiWorkspace:

        analytics_result = self.analytics_service.analyze(portfolio_state)

        # KPI cards
        cards = self.metric_card_presenter.create_cards(
            analytics_result
        )

        # Existing charts
        charts = self.chart_presenter.create_charts(
            analytics_result
        )

        # NEW: Equity curve chart
        if hasattr(portfolio_state, "history") and portfolio_state.history:
            equity_curve = self.equity_curve_presenter.present(
                portfolio_state.history
            )
            charts = [*charts, equity_curve]

        # Sections
        sections = [
            *self.analytics_presenter.create_sections(
                analytics_result
            ),
            *self.portfolio_presenter.create_sections(
                portfolio_state
            ),
        ]

        return GuiWorkspace(
            cards=cards,
            charts=charts,
            sections=sections,
        )