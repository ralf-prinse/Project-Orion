from services.paper_trading.models import PaperTradingResult
from ui.foundation.models import GuiMetric, GuiSection


class PaperTradingPresenter:
    """
    Builds display-only paper trading sections for the GUI.

    This presenter consumes a completed PaperTradingResult from the deterministic
    Paper Trading Engine and projects it into stable GUI sections. It never
    executes trades, changes account state, calculates signals or makes trading
    decisions.
    """

    def create_sections(self, result: PaperTradingResult) -> list[GuiSection]:
        sections = [
            self._create_account_section(result),
            self._create_open_positions_section(result),
            self._create_execution_section(result),
        ]

        diagnostics = self._create_diagnostics_section(result)
        if diagnostics is not None:
            sections.append(diagnostics)

        return sections

    def _create_account_section(self, result: PaperTradingResult) -> GuiSection:
        return GuiSection(
            title="Paper Trading Account",
            description="Virtual account summary from the deterministic paper trading layer.",
            metrics=[
                GuiMetric("Operation", result.operation or "UNKNOWN"),
                GuiMetric("Valid Operation", "Yes" if result.valid_operation else "No"),
                GuiMetric("Cash Balance", f"{result.cash_balance:.2f}"),
                GuiMetric("Equity", f"{result.equity:.2f}"),
                GuiMetric("Currency", result.account.currency),
            ],
        )

    def _create_open_positions_section(self, result: PaperTradingResult) -> GuiSection:
        return GuiSection(
            title="Open Paper Positions",
            description="Current virtual exposure and unrealized performance.",
            metrics=[
                GuiMetric("Open Positions", str(result.open_positions)),
                GuiMetric("Position Value", f"{result.account.total_position_value():.2f}"),
                GuiMetric("Unrealized P/L", f"{result.unrealized_pnl:.2f}"),
                GuiMetric("Realized P/L", f"{result.realized_pnl:.2f}"),
            ],
        )

    def _create_execution_section(self, result: PaperTradingResult) -> GuiSection:
        trade = result.executed_trade

        if trade is None:
            metrics = [
                GuiMetric("Executed Trade", "None"),
                GuiMetric("Trade Status", "N/A"),
                GuiMetric("Symbol", "N/A"),
                GuiMetric("Quantity", "0"),
            ]
        else:
            metrics = [
                GuiMetric("Executed Trade", trade.action),
                GuiMetric("Trade Status", trade.status),
                GuiMetric("Symbol", trade.symbol),
                GuiMetric("Quantity", str(trade.quantity)),
                GuiMetric("Entry Price", f"{trade.entry_price:.2f}"),
                GuiMetric("Exit Price", f"{trade.exit_price:.2f}"),
                GuiMetric("Gross P/L", f"{trade.gross_pnl:.2f}"),
                GuiMetric("Reason", trade.reason or "N/A"),
            ]

        return GuiSection(
            title="Paper Trade Execution",
            description="Latest virtual execution result from Paper Trading Engine.",
            metrics=metrics,
        )

    def _create_diagnostics_section(self, result: PaperTradingResult) -> GuiSection | None:
        diagnostics: list[GuiMetric] = []

        for index, warning in enumerate(result.warnings, start=1):
            diagnostics.append(GuiMetric(f"Warning {index}", warning))

        for index, reason in enumerate(result.reasons, start=1):
            diagnostics.append(GuiMetric(f"Reason {index}", reason))

        if not diagnostics:
            return None

        return GuiSection(
            title="Paper Trading Diagnostics",
            description="Deterministic warnings and reasons from the paper trading layer.",
            metrics=diagnostics,
        )
