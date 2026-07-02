from services.orchestration.ai_market_scanner import AIMarketScanResult
from ui.foundation.models import GuiMetric, GuiSection


class AIScannerPresenter:
    """
    Converts AIMarketScanResult into UI-safe GuiSection objects.

    Presentation logic only.
    No scanning logic.
    No trading calculations.
    """

    def create_sections(
        self,
        scan_result: AIMarketScanResult,
        max_items: int = 10,
    ) -> list[GuiSection]:

        sections: list[GuiSection] = []

        sections.append(
            GuiSection(
                title="AI Scanner Summary",
                description=(
                    f"Scanned {scan_result.total_scanned} of "
                    f"{scan_result.total_requested} symbols. "
                    f"Failed: {scan_result.total_failed}."
                ),
                metrics=[
                    GuiMetric(
                        label="Best Trade",
                        value=(
                            scan_result.best_trade.symbol
                            if scan_result.best_trade
                            else "-"
                        ),
                        helper_text=(
                            scan_result.best_trade.decision
                            if scan_result.best_trade
                            else "No trade available"
                        ),
                    ),
                    GuiMetric(
                        label="Total Scanned",
                        value=str(scan_result.total_scanned),
                    ),
                    GuiMetric(
                        label="Failed",
                        value=str(scan_result.total_failed),
                    ),
                ],
            )
        )

        ranked_items = scan_result.ranked[:max_items]

        for index, item in enumerate(ranked_items, start=1):
            sections.append(
                GuiSection(
                    title=f"#{index} — {item.symbol}",
                    description=item.explanation,
                    metrics=[
                        GuiMetric(
                            label="Decision",
                            value=item.decision,
                        ),
                        GuiMetric(
                            label="Confidence",
                            value=f"{item.confidence:.1%}",
                        ),
                        GuiMetric(
                            label="Pressure",
                            value=f"{item.pressure_score:.3f}",
                        ),
                        GuiMetric(
                            label="Strength",
                            value=f"{item.strength:.3f}",
                        ),
                        GuiMetric(
                            label="Position Size",
                            value=f"{item.position_size:.2f}",
                        ),
                        GuiMetric(
                            label="Risk",
                            value=f"{item.risk_score:.4f}",
                        ),
                    ],
                )
            )

        if scan_result.failed_symbols:
            sections.append(
                GuiSection(
                    title="Failed Symbols",
                    description=", ".join(scan_result.failed_symbols),
                )
            )

        return sections