from services.decisions.models import DecisionResult
from ui.foundation.models import GuiMetric, GuiSection


class DecisionPresenter:
    """
    Builds display-only decision dashboard sections for the GUI.

    The presenter consumes deterministic DecisionResult objects and projects
    them into stable GUI sections. It never validates signals, assembles
    decisions, calculates position sizing or changes portfolio state.
    """

    def create_sections(self, decision_result: DecisionResult) -> list[GuiSection]:
        sections = [
            self._create_summary_section(decision_result),
            self._create_position_section(decision_result),
        ]

        diagnostics = self._create_diagnostics_section(decision_result)
        if diagnostics is not None:
            sections.append(diagnostics)

        return sections

    def _create_summary_section(self, decision_result: DecisionResult) -> GuiSection:
        return GuiSection(
            title="Decision Dashboard",
            description="High-level deterministic output from the Decision Layer.",
            metrics=[
                GuiMetric("Symbol", decision_result.symbol.upper() or "N/A"),
                GuiMetric("Action", decision_result.action.value),
                GuiMetric("Confidence", str(decision_result.confidence)),
                GuiMetric("Risk Level", str(decision_result.risk_level)),
            ],
        )

    def _create_position_section(self, decision_result: DecisionResult) -> GuiSection:
        sizing = decision_result.position_sizing

        metrics = [
            GuiMetric("Position Size", f"{decision_result.position_size:.2f}"),
        ]

        if sizing is None:
            metrics.extend(
                [
                    GuiMetric("Recommended Shares", "0"),
                    GuiMetric("Position Value", "0.00"),
                    GuiMetric("Risk Amount", "0.00"),
                    GuiMetric("Sizing Method", "N/A"),
                ]
            )
        else:
            metrics.extend(
                [
                    GuiMetric("Recommended Shares", str(sizing.recommended_shares)),
                    GuiMetric("Position Value", f"{sizing.position_value:.2f}"),
                    GuiMetric("Risk Amount", f"{sizing.risk_amount:.2f}"),
                    GuiMetric("Risk Per Share", f"{sizing.risk_per_share:.2f}"),
                    GuiMetric("Capital Used", f"{sizing.capital_used:.2f}"),
                    GuiMetric("Sizing Method", sizing.sizing_method),
                ]
            )

        return GuiSection(
            title="Decision Position Sizing",
            description="Position sizing already calculated by deterministic decision services.",
            metrics=metrics,
        )

    def _create_diagnostics_section(self, decision_result: DecisionResult) -> GuiSection | None:
        diagnostics: list[GuiMetric] = []

        for index, reason in enumerate(decision_result.reasons, start=1):
            diagnostics.append(GuiMetric(f"Reason {index}", reason))

        for index, warning in enumerate(decision_result.warnings, start=1):
            diagnostics.append(GuiMetric(f"Warning {index}", warning))

        if decision_result.position_sizing is not None:
            for index, warning in enumerate(decision_result.position_sizing.warnings, start=1):
                diagnostics.append(GuiMetric(f"Sizing Warning {index}", warning))

        if not diagnostics:
            return None

        return GuiSection(
            title="Decision Diagnostics",
            description="Deterministic reasons and warnings from the Decision Layer.",
            metrics=diagnostics,
        )
