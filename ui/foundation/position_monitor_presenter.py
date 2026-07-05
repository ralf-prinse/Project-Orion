from dataclasses import dataclass

from models.trade_lifecycle import ExitSignal


@dataclass(frozen=True)
class PositionMonitorViewModel:
    title: str
    signal: str
    signal_explanation: str
    exit_score: str
    exit_score_explanation: str
    profit_loss: str
    profit_loss_explanation: str
    market_value: str
    risk_status: str
    target_status: str
    intelligence_summary: str
    summary: str
    status: str


class PositionMonitorPresenter:
    """
    Presentation-only formatter for Position Monitor results.

    No trading logic.
    No AI.
    No calculations beyond formatting labels.
    """

    def present(self, result) -> PositionMonitorViewModel:
        trade = result.trade

        return PositionMonitorViewModel(
            title=f"{trade.symbol} Position Monitor",
            signal=self._signal_label(result.exit_signal),
            signal_explanation=result.reason,
            exit_score=f"{result.exit_score}/100",
            exit_score_explanation=self._exit_score_explanation(result.exit_score),
            profit_loss=self._format_profit_loss(
                result.unrealized_profit_loss,
                result.unrealized_profit_loss_percent,
            ),
            profit_loss_explanation=self._profit_loss_explanation(
                result.unrealized_profit_loss,
            ),
            market_value=f"€{result.market_value:,.2f}",
            risk_status=self._risk_status(result),
            target_status=self._target_status(result),
            intelligence_summary=self._intelligence_summary(result),
            summary=self._summary(result),
            status="Position monitor uitgevoerd.",
        )

    def _signal_label(self, signal: ExitSignal) -> str:
        if signal == ExitSignal.STOP_LOSS:
            return "VERKOPEN — Stop-loss geraakt"

        if signal == ExitSignal.TAKE_PROFIT:
            return "VERKOPEN — Winstdoel bereikt"

        if signal == ExitSignal.TRAILING_STOP:
            return "VERKOPEN — Trailing stop geraakt"

        if signal == ExitSignal.EXIT_DUE_TO_WEAKNESS:
            return "VERKOPEN — Setup verzwakt"

        if signal == ExitSignal.EXIT_DUE_TO_TIME_LIMIT:
            return "VERKOPEN — Tijdslimiet bereikt"

        return "VASTHOUDEN"

    def _exit_score_explanation(self, score: int) -> str:
        if score >= 90:
            return "Zeer sterke exit-trigger. Orion adviseert direct actie."

        if score >= 70:
            return "Sterke exit-waarschuwing. De tradekwaliteit verslechtert."

        if score >= 40:
            return "Matige exit-waarschuwing. Blijf de positie actief volgen."

        if score > 0:
            return "Lage exit-druk. Er zijn aandachtspunten, maar geen directe exit."

        return "Geen exit-druk. Stop-loss en winstdoel zijn niet geraakt."

    def _format_profit_loss(self, value: float, percent: float) -> str:
        sign = "+" if value >= 0 else ""
        return f"{sign}€{value:,.2f} ({sign}{percent:.2f}%)"

    def _profit_loss_explanation(self, value: float) -> str:
        if value > 0:
            return "De positie staat momenteel op winst."

        if value < 0:
            return "De positie staat momenteel op verlies."

        return "De positie staat momenteel ongeveer gelijk."

    def _risk_status(self, result) -> str:
        if result.exit_signal == ExitSignal.STOP_LOSS:
            return "Stop-loss geraakt. Risico is actief geworden."

        return (
            f"Afstand tot stop-loss: €{result.stop_loss_distance:,.2f} "
            "per aandeel."
        )

    def _target_status(self, result) -> str:
        if result.exit_signal == ExitSignal.TAKE_PROFIT:
            return "Winstdoel bereikt."

        return (
            f"Afstand tot winstdoel: €{result.take_profit_distance:,.2f} "
            "per aandeel."
        )

    def _intelligence_summary(self, result) -> str:
        lines = [
            f"Trend: {result.trend_status}",
            f"Momentum: {result.momentum_status}",
            f"Risico: {result.risk_status}",
        ]

        if result.exit_reasons:
            lines.append("")
            lines.append("Exit-redenen:")

            for reason in result.exit_reasons:
                lines.append(f"• {reason}")
        else:
            lines.append("")
            lines.append("Exit-redenen:")
            lines.append("• Geen directe exit-trigger gevonden.")

        return "\n".join(lines)

    def _summary(self, result) -> str:
        trade = result.trade

        return (
            f"Entry: €{trade.entry_price:,.2f} | "
            f"Huidige koers: €{trade.current_price:,.2f} | "
            f"Stop-loss: €{trade.stop_loss:,.2f} | "
            f"Winstdoel: €{trade.take_profit:,.2f}"
        )