from ui.foundation.models import GuiMetricCard


class DashboardWorkspacePresenter:
    """
    Presentation-only transformer for dashboard UI.

    Converts deterministic backend state into UI cards.
    No trading logic allowed.
    """

    def create_cards(self, portfolio_state) -> list[GuiMetricCard]:
        cash = getattr(portfolio_state, "cash", 0.0)

        positions = getattr(portfolio_state, "positions", {}) or {}

        equity = cash

        # compute equity safely from positions
        for symbol, position in positions.items():

            if isinstance(position, dict):
                qty = position.get("quantity", 0)
                avg_price = position.get("average_price", 0)
            else:
                qty = getattr(position, "quantity", 0)
                avg_price = getattr(position, "average_price", 0)

            equity += qty * avg_price

        return [
            GuiMetricCard(
                title="Portfolio Value",
                value=f"€ {equity:.2f}",
                subtitle="Totale waarde (cash + posities)",
                trend="Live berekend uit portfolio state",
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
                subtitle="Aantal open posities",
                trend="Uit Portfolio.positions",
            ),
        ]