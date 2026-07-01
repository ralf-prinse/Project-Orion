from services.portfolio.models import PortfolioResult, PortfolioState
from ui.foundation.models import GuiMetric, GuiSection


class PortfolioPresenter:
    """
    Builds display-only portfolio sections for the GUI.

    The presenter consumes deterministic PortfolioState and PortfolioResult
    objects and projects them into stable GUI sections. It never calculates
    portfolio validation, exposure limits, position sizing, risk outcomes or
    trade decisions.
    """

    def create_sections(
        self,
        portfolio_state: PortfolioState,
        portfolio_result: PortfolioResult | None = None,
    ) -> list[GuiSection]:
        sections = [
            self._create_account_section(portfolio_state),
            self._create_positions_section(portfolio_state),
        ]

        if portfolio_result is not None:
            sections.append(self._create_validation_section(portfolio_result))

        return sections

    def _create_account_section(self, portfolio_state: PortfolioState) -> GuiSection:
        return GuiSection(
            title="Portfolio Account",
            description="Display-only account values supplied by the Portfolio Engine.",
            metrics=[
                GuiMetric("Cash", f"{portfolio_state.cash:.2f}"),
                GuiMetric("Position Value", f"{portfolio_state.total_position_value():.2f}"),
                GuiMetric("Total Value", f"{portfolio_state.total_value():.2f}"),
                GuiMetric("Currency", portfolio_state.currency),
            ],
        )

    def _create_positions_section(self, portfolio_state: PortfolioState) -> GuiSection:
        if not portfolio_state.positions:
            return GuiSection(
                title="Open Positions",
                description="No open portfolio positions are available.",
                metrics=[GuiMetric("Positions", "0")],
            )

        metrics: list[GuiMetric] = [
            GuiMetric("Open Positions", str(portfolio_state.open_position_count()))
        ]

        for symbol in sorted(portfolio_state.positions.keys()):
            position = portfolio_state.positions[symbol]
            metrics.extend(
                [
                    GuiMetric(f"{symbol} Quantity", str(position.quantity)),
                    GuiMetric(f"{symbol} Average Price", f"{position.average_price:.2f}"),
                    GuiMetric(f"{symbol} Current Price", self._format_optional_price(position.current_price)),
                    GuiMetric(f"{symbol} Market Value", f"{position.market_value():.2f}"),
                ]
            )

            if position.sector:
                metrics.append(GuiMetric(f"{symbol} Sector", position.sector))

        return GuiSection(
            title="Open Positions",
            description="Presentation view of current portfolio positions.",
            metrics=metrics,
        )

    def _create_validation_section(self, portfolio_result: PortfolioResult) -> GuiSection:
        metrics = [
            GuiMetric("Symbol", portfolio_result.symbol or "N/A"),
            GuiMetric("Portfolio Allowed", self._format_bool(portfolio_result.portfolio_allowed)),
            GuiMetric("Cash Sufficient", self._format_bool(portfolio_result.cash_sufficient)),
            GuiMetric("Position Limit Allowed", self._format_bool(portfolio_result.position_limit_allowed)),
            GuiMetric("Existing Position Allowed", self._format_bool(portfolio_result.existing_position_allowed)),
            GuiMetric("Exposure Allowed", self._format_bool(portfolio_result.exposure_allowed)),
            GuiMetric("Position Exposure", f"{portfolio_result.position_exposure:.4f}"),
            GuiMetric("Total Exposure", f"{portfolio_result.total_exposure:.4f}"),
            GuiMetric("Proposed Position Value", f"{portfolio_result.proposed_position_value:.2f}"),
        ]

        for index, reason in enumerate(portfolio_result.reasons, start=1):
            metrics.append(GuiMetric(f"Reason {index}", reason))

        for index, warning in enumerate(portfolio_result.warnings, start=1):
            metrics.append(GuiMetric(f"Warning {index}", warning))

        return GuiSection(
            title="Portfolio Validation",
            description="Deterministic portfolio validation result projected for the GUI.",
            metrics=metrics,
        )

    def _format_optional_price(self, value: float | None) -> str:
        if value is None:
            return "N/A"

        return f"{value:.2f}"

    def _format_bool(self, value: bool) -> str:
        return "Yes" if value else "No"
