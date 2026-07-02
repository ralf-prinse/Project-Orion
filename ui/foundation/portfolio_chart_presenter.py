from services.portfolio.analytics_models import PortfolioAnalyticsResult
from ui.foundation.models import GuiChart, GuiChartPoint


class PortfolioChartPresenter:
    """
    Creates portfolio chart presentation models.

    This presenter performs no portfolio calculations. It converts deterministic
    analytics output into presentation-safe GuiChart models.
    """

    def create_charts(
        self,
        analytics_result: PortfolioAnalyticsResult,
    ) -> list[GuiChart]:
        return [
            self._create_allocation_chart(analytics_result),
        ]

    def _create_allocation_chart(
        self,
        analytics_result: PortfolioAnalyticsResult,
    ) -> GuiChart:
        points = [
            GuiChartPoint(
                label="Cash",
                value=float(analytics_result.cash),
            ),
            GuiChartPoint(
                label="Invested",
                value=float(analytics_result.invested_value),
            ),
        ]

        return GuiChart(
            title="Portfolio Allocation",
            description="Verdeling tussen cash en geïnvesteerd vermogen.",
            chart_type="line",
            unit="€",
            points=points,
        )