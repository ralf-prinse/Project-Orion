from services.portfolio.analytics_models import PortfolioAnalyticsResult
from ui.foundation.models import GuiMetric, GuiSection


class PortfolioAnalyticsPresenter:
    """
    Builds display-only portfolio analytics sections for the GUI.

    This presenter consumes deterministic analytics results and converts them
    into GuiSections. It performs no portfolio calculations.
    """

    def create_sections(
        self,
        result: PortfolioAnalyticsResult,
    ) -> list[GuiSection]:
        return [
            GuiSection(
                title="Portfolio Analytics",
                description="Deterministische kerncijfers van de huidige portefeuille.",
                metrics=[
                    GuiMetric("Totale waarde", self._money(result.total_value, result.currency)),
                    GuiMetric("Cash", self._money(result.cash, result.currency)),
                    GuiMetric("Geïnvesteerd", self._money(result.invested_value, result.currency)),
                    GuiMetric("Open posities", str(result.open_positions)),
                    GuiMetric("Totale exposure", self._percentage(result.total_exposure)),
                ],
            ),
            GuiSection(
                title="Position Analytics",
                description="Samenvatting van positieomvang en concentratie.",
                metrics=[
                    GuiMetric(
                        "Gemiddelde positie",
                        self._money(result.average_position_value, result.currency),
                    ),
                    GuiMetric(
                        "Grootste positie",
                        result.largest_position_symbol or "N/A",
                    ),
                    GuiMetric(
                        "Waarde grootste positie",
                        self._money(result.largest_position_value, result.currency),
                    ),
                ],
            ),
        ]

    def _money(self, value: float, currency: str) -> str:
        return f"{currency} {value:.2f}"

    def _percentage(self, value: float) -> str:
        return f"{value * 100:.2f}%"