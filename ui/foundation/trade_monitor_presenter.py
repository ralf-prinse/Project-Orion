from __future__ import annotations

from dataclasses import dataclass

from models.trade_lifecycle import Trade


@dataclass(frozen=True)
class TradeMonitorListViewModel:
    title: str
    summary: str
    trades_text: str
    status: str


class TradeMonitorPresenter:
    """
    Presentation-only formatter for Trade Monitor overview.

    No business logic.
    No persistence.
    No exit decisions.
    """

    def present_open_trades(
        self,
        trades: list[Trade],
    ) -> TradeMonitorListViewModel:
        if not trades:
            return TradeMonitorListViewModel(
                title="Open Trades",
                summary="Geen open trades gevonden.",
                trades_text="Er zijn momenteel geen open trades opgeslagen.",
                status="Trade Monitor geladen.",
            )

        lines: list[str] = []

        for index, trade in enumerate(trades, start=1):
            lines.extend(self._format_trade(index, trade))

        return TradeMonitorListViewModel(
            title="Open Trades",
            summary=f"{len(trades)} open trade(s) actief.",
            trades_text="\n".join(lines).strip(),
            status="Open trades geladen.",
        )

    def _format_trade(
        self,
        index: int,
        trade: Trade,
    ) -> list[str]:
        pnl_icon = self._pnl_icon(trade)
        exit_icon = self._exit_icon(trade)

        target_1 = trade.target_1 or trade.take_profit
        confidence_percent = trade.risk_plan_confidence * 100

        progress_to_target_1 = self._progress_to_target(
            trade=trade,
            target=target_1,
        )

        progress_bar = self._progress_bar(progress_to_target_1)

        return [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"{index}. {trade.symbol}   🟢 OPEN",
            "",
            "Prijs & positie",
            f"   Aantal:        {trade.quantity}",
            f"   Entry:         €{trade.entry_price:,.2f}",
            f"   Huidige koers: €{trade.current_price:,.2f}",
            (
                f"   {pnl_icon} P/L:        "
                f"€{trade.unrealized_profit_loss:,.2f} "
                f"({trade.unrealized_profit_loss_percent:.2f}%)"
            ),
            "",
            "RiskPlan",
            f"   Stop-loss:     €{trade.stop_loss:,.2f}",
            f"   Target 1:      €{target_1:,.2f}",
            f"   Target 2:      €{trade.target_2:,.2f}",
            f"   Target 3:      €{trade.target_3:,.2f}",
            "",
            f"   Risk:          {trade.risk_percent:.2f}%",
            f"   Reward:        {trade.reward_percent:.2f}%",
            f"   Risk/Reward:   {trade.risk_reward_ratio:.2f}",
            f"   Confidence:    {confidence_percent:.0f}%",
            "",
            "Progress",
            f"   Target 1:      {progress_bar} {progress_to_target_1:.0f}%",
            "",
            "Adaptive context",
            f"   {self._format_adaptive_notes(trade.risk_plan_notes)}",
            "",
            f"   {exit_icon} Exit status: {trade.exit_signal.value}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
        ]

    def _progress_to_target(
        self,
        trade: Trade,
        target: float,
    ) -> float:
        if trade.entry_price <= 0:
            return 0.0

        if target <= trade.entry_price:
            return 0.0

        progress = (
            (trade.current_price - trade.entry_price)
            / (target - trade.entry_price)
        ) * 100

        return max(0.0, min(100.0, progress))

    def _progress_bar(
        self,
        progress_percent: float,
    ) -> str:
        filled_blocks = int(round(progress_percent / 10))
        empty_blocks = 10 - filled_blocks

        return "█" * filled_blocks + "░" * empty_blocks

    def _format_adaptive_notes(
        self,
        notes: str,
    ) -> str:
        if not notes:
            return "Geen adaptive risk notes beschikbaar."

        parts = {}

        for item in notes.split("|"):
            if "=" not in item:
                continue

            key, value = item.split("=", 1)
            parts[key.strip().lower()] = value.strip().upper()

        volatility = parts.get("volatility")
        regime = parts.get("regime")
        risk = parts.get("risk")

        formatted: list[str] = []

        if regime:
            formatted.append(f"Regime: {self._regime_label(regime)}")

        if volatility:
            formatted.append(f"Volatiliteit: {self._volatility_label(volatility)}")

        if risk:
            formatted.append(f"Risk score: {risk}")

        if not formatted:
            return notes

        return " | ".join(formatted)

    def _regime_label(
        self,
        regime: str,
    ) -> str:
        if regime == "BULL":
            return "Bullish 🟢"

        if regime == "BEAR":
            return "Bearish 🔴"

        if regime == "SIDEWAYS":
            return "Sideways 🟡"

        return regime.title()

    def _volatility_label(
        self,
        volatility: str,
    ) -> str:
        if volatility == "LOW":
            return "Laag 🟢"

        if volatility in {"NORMAL", "MEDIUM"}:
            return "Normaal 🟡"

        if volatility == "HIGH":
            return "Hoog 🔴"

        return volatility.title()

    def _pnl_icon(self, trade: Trade) -> str:
        if trade.unrealized_profit_loss > 0:
            return "🟢"

        if trade.unrealized_profit_loss < 0:
            return "🔴"

        return "⚪"

    def _exit_icon(self, trade: Trade) -> str:
        value = str(trade.exit_signal.value).upper()

        if value == "HOLD_POSITION":
            return "🟢"

        if value in {"TAKE_PROFIT", "TRAILING_STOP"}:
            return "🟡"

        return "🔴"