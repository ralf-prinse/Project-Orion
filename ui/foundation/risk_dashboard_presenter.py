from services.risk.models import RiskContext, RiskProfile, RiskResult
from ui.foundation.models import GuiMetric, GuiSection


class RiskDashboardPresenter:
    """
    Builds display-only risk dashboard sections for the GUI.

    The presenter consumes deterministic RiskContext, RiskProfile and RiskResult
    objects and projects them into stable GUI sections. It never evaluates risk,
    changes portfolio state, calculates position sizing or makes trading
    decisions.
    """

    def create_sections(
        self,
        risk_result: RiskResult,
        risk_context: RiskContext | None = None,
        risk_profile: RiskProfile | None = None,
    ) -> list[GuiSection]:
        sections = [
            self._create_summary_section(risk_result),
            self._create_limit_status_section(risk_result),
            self._create_risk_metrics_section(risk_result),
        ]

        if risk_context is not None:
            sections.append(self._create_context_section(risk_context))

        if risk_profile is not None:
            sections.append(self._create_profile_section(risk_profile))

        diagnostics = self._create_diagnostics_section(risk_result)
        if diagnostics is not None:
            sections.append(diagnostics)

        return sections

    def _create_summary_section(self, risk_result: RiskResult) -> GuiSection:
        return GuiSection(
            title="Risk Dashboard",
            description="High-level risk outcome from the deterministic Risk Manager.",
            metrics=[
                GuiMetric("Symbol", risk_result.symbol or "N/A"),
                GuiMetric("Risk Allowed", self._format_bool(risk_result.risk_allowed)),
                GuiMetric("Portfolio Value", f"{risk_result.portfolio_value:.2f}"),
            ],
        )

    def _create_limit_status_section(self, risk_result: RiskResult) -> GuiSection:
        return GuiSection(
            title="Risk Limit Status",
            description="Pass/fail status for deterministic risk constraints.",
            metrics=[
                GuiMetric("Trade Risk Allowed", self._format_bool(risk_result.trade_risk_allowed)),
                GuiMetric("Portfolio Risk Allowed", self._format_bool(risk_result.portfolio_risk_allowed)),
                GuiMetric("Drawdown Allowed", self._format_bool(risk_result.drawdown_allowed)),
                GuiMetric("Capital Protection Allowed", self._format_bool(risk_result.capital_protection_allowed)),
                GuiMetric("Position Exposure Allowed", self._format_bool(risk_result.position_exposure_allowed)),
            ],
        )

    def _create_risk_metrics_section(self, risk_result: RiskResult) -> GuiSection:
        return GuiSection(
            title="Risk Metrics",
            description="Risk ratios calculated before the GUI receives the result.",
            metrics=[
                GuiMetric("Proposed Risk Ratio", f"{risk_result.proposed_risk_ratio:.4f}"),
                GuiMetric("Total Portfolio Risk", f"{risk_result.total_portfolio_risk:.4f}"),
                GuiMetric("Drawdown", f"{risk_result.drawdown:.4f}"),
                GuiMetric("Cash Reserve After Trade", f"{risk_result.cash_reserve_after_trade:.4f}"),
                GuiMetric("Position Exposure", f"{risk_result.position_exposure:.4f}"),
            ],
        )

    def _create_context_section(self, risk_context: RiskContext) -> GuiSection:
        return GuiSection(
            title="Risk Context",
            description="Input values supplied to the Risk Manager.",
            metrics=[
                GuiMetric("Symbol", risk_context.symbol.upper() or "N/A"),
                GuiMetric("Portfolio Value", f"{risk_context.portfolio_value:.2f}"),
                GuiMetric("Cash Available", f"{risk_context.cash_available:.2f}"),
                GuiMetric("Current Portfolio Risk", f"{risk_context.current_portfolio_risk:.4f}"),
                GuiMetric("Proposed Position Value", f"{risk_context.proposed_position_value:.2f}"),
                GuiMetric("Proposed Risk Amount", f"{risk_context.proposed_risk_amount:.2f}"),
            ],
        )

    def _create_profile_section(self, risk_profile: RiskProfile) -> GuiSection:
        return GuiSection(
            title="Risk Profile",
            description="Configured deterministic risk limits.",
            metrics=[
                GuiMetric("Max Risk Per Trade", f"{risk_profile.max_risk_per_trade:.4f}"),
                GuiMetric("Max Portfolio Risk", f"{risk_profile.max_portfolio_risk:.4f}"),
                GuiMetric("Max Drawdown", f"{risk_profile.max_drawdown:.4f}"),
                GuiMetric("Minimum Cash Reserve", f"{risk_profile.min_cash_reserve:.4f}"),
                GuiMetric("Max Position Exposure", f"{risk_profile.max_position_exposure:.4f}"),
            ],
        )

    def _create_diagnostics_section(self, risk_result: RiskResult) -> GuiSection | None:
        diagnostics: list[GuiMetric] = []

        for index, reason in enumerate(risk_result.reasons, start=1):
            diagnostics.append(GuiMetric(f"Reason {index}", reason))

        for index, warning in enumerate(risk_result.warnings, start=1):
            diagnostics.append(GuiMetric(f"Warning {index}", warning))

        if not diagnostics:
            return None

        return GuiSection(
            title="Risk Diagnostics",
            description="Deterministic warnings and reasons from the Risk Manager.",
            metrics=diagnostics,
        )

    def _format_bool(self, value: bool) -> str:
        return "Yes" if value else "No"
