from services.portfolio.analytics_models import PortfolioAnalyticsResult
from ui.foundation.models import GuiMetricCard


class PortfolioMetricCardPresenter:
    """
    Builds display-only KPI cards for the Portfolio workspace.

    This presenter consumes deterministic portfolio analytics results and
    converts them into GuiMetricCard models. It performs no calculations.
    """

    def create_cards(
        self,
        result: PortfolioAnalyticsResult,
    ) -> list[GuiMetricCard]:
        return [
            GuiMetricCard(
                title="Totale waarde",
                value=self._money(result.total_value, result.currency),
                subtitle="Portfolio value",
            ),
            GuiMetricCard(
                title="Cash",
                value=self._money(result.cash, result.currency),
                subtitle="Beschikbaar kapitaal",
            ),
            GuiMetricCard(
                title="Exposure",
                value=self._percentage(result.total_exposure),
                subtitle="Geïnvesteerd vermogen",
            ),
            GuiMetricCard(
                title="Open posities",
                value=str(result.open_positions),
                subtitle="Actieve posities",
            ),
        ]

    def _money(self, value: float, currency: str) -> str:
        return f"{currency} {value:.2f}"

    def _percentage(self, value: float) -> str:
        return f"{value * 100:.2f}%"