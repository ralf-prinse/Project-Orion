from services.planner.models import TradePlanResult
from ui.foundation.models import GuiMetric, GuiSection


class TradePlanPresenter:
    """
    Builds display-only trade plan sections for the GUI.

    This presenter consumes a completed TradePlanResult from the deterministic
    Trade Planner and projects it into stable GUI sections. It never calculates
    entries, stops, targets, reward/risk ratios, position sizes or trading
    decisions.
    """

    def create_sections(self, result: TradePlanResult) -> list[GuiSection]:
        sections = [
            self._create_summary_section(result),
            self._create_price_plan_section(result),
            self._create_position_section(result),
            self._create_reward_risk_section(result),
        ]

        diagnostics = self._create_diagnostics_section(result)
        if diagnostics is not None:
            sections.append(diagnostics)

        return sections

    def _create_summary_section(self, result: TradePlanResult) -> GuiSection:
        return GuiSection(
            title="Trade Plan Summary",
            description="High-level trade plan produced by the deterministic Trade Planner.",
            metrics=[
                GuiMetric("Symbol", result.symbol or "N/A"),
                GuiMetric("Action", result.action or "NONE"),
                GuiMetric("Valid Plan", "Yes" if result.valid_plan else "No"),
                GuiMetric("Currency", result.currency),
            ],
        )

    def _create_price_plan_section(self, result: TradePlanResult) -> GuiSection:
        return GuiSection(
            title="Entry, Stop & Target",
            description="Executable price levels calculated before the GUI receives the result.",
            metrics=[
                GuiMetric("Entry Price", f"{result.entry_price:.2f}"),
                GuiMetric("Stop Loss", f"{result.stop_loss:.2f}"),
                GuiMetric("Target Price", f"{result.target_price:.2f}"),
                GuiMetric("Risk Per Share", f"{result.risk_per_share:.2f}"),
            ],
        )

    def _create_position_section(self, result: TradePlanResult) -> GuiSection:
        return GuiSection(
            title="Planned Position",
            description="Position details supplied by deterministic sizing and planning layers.",
            metrics=[
                GuiMetric("Shares", str(result.shares)),
                GuiMetric("Position Value", f"{result.position_value:.2f}"),
                GuiMetric("Total Risk", f"{result.total_risk_amount:.2f}"),
            ],
        )

    def _create_reward_risk_section(self, result: TradePlanResult) -> GuiSection:
        return GuiSection(
            title="Reward / Risk",
            description="Reward and risk metrics calculated by the Trade Planner.",
            metrics=[
                GuiMetric("Expected Reward / Share", f"{result.expected_reward_per_share:.2f}"),
                GuiMetric("Expected Reward", f"{result.expected_reward_amount:.2f}"),
                GuiMetric("Reward/Risk Ratio", f"{result.reward_risk_ratio:.2f}"),
            ],
        )

    def _create_diagnostics_section(self, result: TradePlanResult) -> GuiSection | None:
        diagnostics: list[GuiMetric] = []

        for index, warning in enumerate(result.warnings, start=1):
            diagnostics.append(GuiMetric(f"Warning {index}", warning))

        for index, reason in enumerate(result.reasons, start=1):
            diagnostics.append(GuiMetric(f"Reason {index}", reason))

        if not diagnostics:
            return None

        return GuiSection(
            title="Trade Plan Diagnostics",
            description="Deterministic warnings and reasons from the Trade Planner.",
            metrics=diagnostics,
        )
