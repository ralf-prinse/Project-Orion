from typing import Any

from ui.foundation.models import GuiMetric, GuiSection


class TradeAdvicePresenter:
    """
    Builds display-only trade advice sections for the GUI.

    The presenter consumes deterministic trade plan objects and projects them
    into stable GuiSection models. It never creates signals, makes decisions,
    calculates risk, sizes positions or executes trades.
    """

    def create_sections(
        self,
        trade_plans: list[Any],
        managed_trades: list[Any] | None = None,
    ) -> list[GuiSection]:
        buy_plans = self._filter_by_action(trade_plans, "BUY")
        hold_plans = self._filter_by_action(trade_plans, "HOLD")
        sell_plans = self._filter_by_action(trade_plans, "SELL")

        sections = [
            self._create_summary_section(
                buy_count=len(buy_plans),
                hold_count=len(hold_plans),
                sell_count=len(sell_plans),
                managed_count=len(managed_trades or []),
            )
        ]

        if buy_plans:
            sections.append(self._create_action_section("Buy Candidates", buy_plans))

        if hold_plans:
            sections.append(self._create_action_section("Hold Candidates", hold_plans))

        if sell_plans:
            sections.append(self._create_action_section("Sell Candidates", sell_plans))

        return sections

    def _create_summary_section(
        self,
        buy_count: int,
        hold_count: int,
        sell_count: int,
        managed_count: int,
    ) -> GuiSection:
        action_count = buy_count + hold_count + sell_count

        if action_count == 0:
            description = (
                "The market scan completed, but no deterministic trade plan "
                "was strong enough for action."
            )
        else:
            description = "Display-only summary of deterministic trade plan actions."

        return GuiSection(
            title="Trade Advice Summary",
            description=description,
            metrics=[
                GuiMetric("Buy", str(buy_count)),
                GuiMetric("Hold", str(hold_count)),
                GuiMetric("Sell", str(sell_count)),
                GuiMetric("Managed Trades", str(managed_count)),
            ],
        )

    def _create_action_section(self, title: str, plans: list[Any]) -> GuiSection:
        metrics: list[GuiMetric] = []

        for plan in plans:
            symbol = getattr(plan, "symbol", "N/A")
            quantity = getattr(plan, "quantity", 0)
            action = getattr(plan, "action", "")

            metrics.append(
                GuiMetric(
                    label=str(symbol),
                    value=f"{str(action).upper()} | Quantity: {quantity}",
                )
            )

        return GuiSection(
            title=title,
            description="Deterministic trade plans projected for display.",
            metrics=metrics,
        )

    def _filter_by_action(self, trade_plans: list[Any], action: str) -> list[Any]:
        return [
            plan
            for plan in trade_plans
            if str(getattr(plan, "action", "")).upper() == action
        ]