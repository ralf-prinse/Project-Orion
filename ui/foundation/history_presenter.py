from ui.foundation.models import GuiMetric, GuiSection


class HistoryPresenter:
    """
    Builds display-only trade history sections for the GUI.

    The presenter formats existing trade history records only. It does not
    execute trades, calculate performance, mutate portfolio state or call
    trading services.
    """

    def create_sections(self, trades: list[dict]) -> list[GuiSection]:
        return [
            self._create_summary_section(trades),
            self._create_recent_trades_section(trades),
        ]

    def _create_summary_section(self, trades: list[dict]) -> GuiSection:
        return GuiSection(
            title="Trade History Summary",
            description="Display-only summary of stored trade events.",
            metrics=[
                GuiMetric("Total Events", str(len(trades))),
            ],
        )

    def _create_recent_trades_section(self, trades: list[dict]) -> GuiSection:
        if not trades:
            return GuiSection(
                title="Recent Trade Events",
                description="No trade events are available.",
                metrics=[GuiMetric("Events", "0")],
            )

        metrics: list[GuiMetric] = []

        for index, trade in enumerate(reversed(trades[-20:]), start=1):
            action = trade.get("action", "UNKNOWN")
            symbol = trade.get("symbol", "")
            quantity = trade.get("quantity", 0)
            price = float(trade.get("price", 0.0))
            timestamp = trade.get("timestamp", "")
            reason = trade.get("reason", "")

            metrics.append(
                GuiMetric(
                    f"Event {index}",
                    f"{action} {symbol} | {quantity} @ {price:.2f}",
                    helper_text=f"{timestamp} {reason}".strip(),
                )
            )

        return GuiSection(
            title="Recent Trade Events",
            description="Most recent stored trade events.",
            metrics=metrics,
        )