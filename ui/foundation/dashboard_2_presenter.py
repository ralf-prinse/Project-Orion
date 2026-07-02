from ui.foundation.dashboard_card_model import DashboardCardModel
from ui.foundation.dashboard_data import DashboardData
from ui.foundation.models import GuiMetric, GuiSection


class Dashboard2Presenter:
    """
    Creates Dashboard 2.0 presentation models.

    Presentation-only.
    """

    def create_cards(self, data: DashboardData | None = None) -> list[DashboardCardModel]:
        if data is None:
            return self.create_default_cards()

        portfolio_state = data.portfolio_state
        portfolio_result = data.portfolio_result
        scanner_result = data.scanner_result

        equity = portfolio_state.total_value() if portfolio_state else 0.0
        cash = portfolio_state.cash if portfolio_state else 0.0
        position_value = portfolio_state.total_position_value() if portfolio_state else 0.0
        open_positions = portfolio_state.open_position_count() if portfolio_state else 0

        exposure = 0.0
        if equity > 0:
            exposure = round((position_value / equity) * 100, 2)

        if portfolio_result is not None:
            exposure = round(portfolio_result.total_exposure * 100, 2)

        best_trade = getattr(scanner_result, "best_trade", None)
        total_scanned = getattr(scanner_result, "total_scanned", 0)
        total_failed = getattr(scanner_result, "total_failed", 0)

        best_symbol = best_trade.symbol if best_trade else "-"
        best_decision = best_trade.decision if best_trade else "No scan yet"
        best_confidence = self._percentage(best_trade.confidence) if best_trade else "0%"

        average_confidence = self._average_confidence(scanner_result)
        market_health = self._market_health(scanner_result)
        pressure_label = self._pressure_label(best_trade)
        risk_score = best_trade.risk_score if best_trade else 0.0

        return [
            DashboardCardModel(
                title="Portfolio Summary",
                value=self._money(equity),
                subtitle=f"Cash: {self._money(cash)} | Open Positions: {open_positions}",
                footer="Live portfolio snapshot.",
            ),
            DashboardCardModel(
                title="Cash Widget",
                value=self._money(cash),
                subtitle="Available portfolio cash.",
                footer="Loaded from PortfolioState.",
            ),
            DashboardCardModel(
                title="Equity Widget",
                value=self._money(equity),
                subtitle=f"Positions: {self._money(position_value)}",
                footer="Cash plus open position value.",
            ),
            DashboardCardModel(
                title="Today's P/L",
                value="€0.00",
                subtitle="Change: 0.00%",
                footer="Daily P/L will connect to performance history later.",
            ),
            DashboardCardModel(
                title="Open Positions",
                value=str(open_positions),
                subtitle=f"Position value: {self._money(position_value)}",
                footer="Current open portfolio positions.",
            ),
            DashboardCardModel(
                title="Portfolio Exposure",
                value=f"{exposure:.2f}%",
                subtitle=f"Cash: {self._money(cash)}",
                footer="Derived from deterministic portfolio state.",
            ),
            DashboardCardModel(
                title="Confidence Gauge",
                value=average_confidence,
                subtitle=f"Best trade confidence: {best_confidence}",
                footer="Based on deterministic scanner output.",
            ),
            DashboardCardModel(
                title="Pressure Gauge",
                value=pressure_label,
                subtitle=f"Best trade: {best_symbol}",
                footer="Based on best ranked scanner item.",
            ),
            DashboardCardModel(
                title="Risk Gauge",
                value=self._risk_label_from_score(risk_score, exposure),
                subtitle=f"Scanner risk: {self._percentage(risk_score)} | Exposure: {exposure:.2f}%",
                footer="Display-only risk indication.",
            ),
            DashboardCardModel(
                title="Best Trade Card",
                value=best_symbol,
                subtitle=f"{best_decision} | Confidence: {best_confidence}",
                footer="Highest ranked deterministic scanner opportunity.",
            ),
            DashboardCardModel(
                title="Market Health",
                value=market_health,
                subtitle=f"Scanned: {total_scanned} | Failed: {total_failed}",
                footer="Summary of current scanner health.",
            ),
            DashboardCardModel(
                title="Portfolio Allocation",
                value=f"Cash {self._cash_percentage(cash, equity):.2f}%",
                subtitle=f"Positions {exposure:.2f}%",
                footer="Portfolio allocation overview.",
            ),
            DashboardCardModel(
                title="Equity Curve",
                value="Waiting",
                subtitle="0 points",
                footer="Historical equity visualization later.",
            ),
        ]

    def create_default_cards(self) -> list[DashboardCardModel]:
        return self.create_cards(DashboardData())

    def create_default_sections(self) -> list[GuiSection]:
        return [
            GuiSection(
                title=card.title,
                description=card.footer,
                metrics=[
                    GuiMetric("Value", card.value),
                    GuiMetric("Info", card.subtitle),
                ],
            )
            for card in self.create_default_cards()
        ]

    def _money(self, value: float) -> str:
        return f"€{value:,.2f}"

    def _percentage(self, value: float) -> str:
        return f"{value * 100:.0f}%"

    def _cash_percentage(self, cash: float, equity: float) -> float:
        if equity <= 0:
            return 100.0
        return round((cash / equity) * 100, 2)

    def _average_confidence(self, scanner_result) -> str:
        ranked = getattr(scanner_result, "ranked", None)

        if not ranked:
            return "0%"

        average = sum(item.confidence for item in ranked) / len(ranked)
        return self._percentage(average)

    def _market_health(self, scanner_result) -> str:
        if scanner_result is None:
            return "Unknown"

        total_scanned = getattr(scanner_result, "total_scanned", 0)
        total_failed = getattr(scanner_result, "total_failed", 0)
        best_trade = getattr(scanner_result, "best_trade", None)

        if total_scanned <= 0:
            return "No Data"

        failure_ratio = total_failed / max(total_scanned + total_failed, 1)

        if failure_ratio >= 0.5:
            return "Weak"

        if best_trade and best_trade.decision == "BUY" and best_trade.confidence >= 0.7:
            return "Strong"

        if best_trade and best_trade.confidence >= 0.55:
            return "Neutral"

        return "Cautious"

    def _pressure_label(self, best_trade) -> str:
        if best_trade is None:
            return "Neutral"

        if best_trade.buy_pressure > best_trade.sell_pressure:
            return "Buy Pressure"

        if best_trade.sell_pressure > best_trade.buy_pressure:
            return "Sell Pressure"

        return "Neutral"

    def _risk_label_from_score(self, risk_score: float, exposure: float) -> str:
        if risk_score >= 0.70 or exposure >= 80:
            return "High"

        if risk_score >= 0.40 or exposure >= 50:
            return "Medium"

        return "Low"