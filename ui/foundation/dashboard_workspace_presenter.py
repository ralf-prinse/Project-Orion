from ui.foundation.models import GuiMetricCard
from ui.foundation.workspace import GuiWorkspace

from ui.foundation.charts import (
    GuiChart,
    GuiChartType,
    GuiSeries,
    GuiAxis,
    GuiLegend,
)


class DashboardWorkspacePresenter:
    """
    Presentation-only dashboard transformer.

    Converts deterministic backend/provider output into GuiWorkspace objects.
    No trading logic.
    No AI calculations.
    """

    def create_workspace(
        self,
        portfolio_state=None,
        chart_title: str = "Market Price Curve",
        chart_subtitle: str = "Klik op Analyseer markt om actuele marktdata op te halen.",
        chart_values: list[float] | None = None,
        symbol: str = "SPY",
        period_label: str = "3 maanden",
        source_label: str = "Yahoo Finance",
    ) -> GuiWorkspace:
        cards = self.create_cards(portfolio_state)
        charts = []

        values = chart_values or []

        if values:
            chart = self._create_price_chart(
                values=values,
                symbol=symbol,
                period_label=period_label,
                source_label=source_label,
                title=chart_title,
                subtitle=chart_subtitle,
            )

            charts.append(chart)

        return GuiWorkspace(
            title="Dashboard",
            subtitle="",
            cards=cards,
            charts=charts,
            chart_sections=[],
            sections=[],
            status="neutral",
            metadata={},
        )

    def create_default_workspace(self) -> GuiWorkspace:
        return self.create_workspace(
            portfolio_state=None,
            chart_title="Market Price Curve",
            chart_subtitle="Klik op Analyseer markt om actuele marktdata op te halen.",
            chart_values=[],
            symbol="SPY",
            period_label="3 maanden",
            source_label="Yahoo Finance",
        )

    def create_cards(self, portfolio_state) -> list[GuiMetricCard]:
        cash = getattr(portfolio_state, "cash", 0.0)
        positions = getattr(portfolio_state, "positions", {}) or {}

        equity = cash

        for _, position in positions.items():
            if isinstance(position, dict):
                qty = position.get("quantity", 0)
                price = position.get("average_price", 0)
            else:
                qty = getattr(position, "quantity", 0)
                price = getattr(position, "average_price", 0)

            equity += qty * price

        return [
            GuiMetricCard(
                title="Portfolio Value",
                value=f"€ {equity:.2f}",
                subtitle="Totale waarde (cash + posities)",
                trend="Berekend uit portfolio state",
            ),
            GuiMetricCard(
                title="Cash",
                value=f"€ {cash:.2f}",
                subtitle="Beschikbare liquiditeit",
                trend="Direct uit Portfolio.cash",
            ),
            GuiMetricCard(
                title="Positions",
                value=str(len(positions)),
                subtitle="Aantal posities",
                trend="Uit Portfolio.positions",
            ),
        ]

    def _create_price_chart(
        self,
        values: list[float],
        symbol: str,
        period_label: str,
        source_label: str,
        title: str,
        subtitle: str,
    ) -> GuiChart:
        first_value = values[0]
        last_value = values[-1]
        high_value = max(values)
        low_value = min(values)

        change_percentage = 0.0

        if first_value != 0:
            change_percentage = ((last_value - first_value) / first_value) * 100

        series = GuiSeries(
            name=f"{symbol} Close",
            values=values,
            labels=[],
            metadata={
                "symbol": symbol,
                "period": period_label,
                "source": source_label,
            },
        )

        return GuiChart(
            title=f"{symbol} • Price Curve",
            chart_type=GuiChartType.LINE,
            series=[series],
            subtitle=f"{period_label} • {source_label} • Close-prijzen",
            x_axis=GuiAxis(label="Periode"),
            y_axis=GuiAxis(label="Prijs"),
            legend=GuiLegend(visible=True),
            status="neutral",
            metadata={
                "status_label": "Laatste scan-data",
                "last_value": f"{last_value:.2f}",
                "change_percentage": f"{change_percentage:+.2f}%",
                "high_value": f"{high_value:.2f}",
                "low_value": f"{low_value:.2f}",
                "data_points": str(len(values)),
                "source": source_label,
                "symbol": symbol,
                "period": period_label,
            },
        )