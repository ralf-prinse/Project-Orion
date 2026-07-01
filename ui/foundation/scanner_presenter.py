from typing import Any

from ui.foundation.models import GuiMetric, GuiSection


class ScannerPresenter:
    """
    Builds display-only scanner sections for the GUI.

    This presenter consumes completed scanner result objects from the
    deterministic scanner pipeline and projects them into stable GUI sections.
    It uses presentation-safe duck typing so importing the GUI does not import
    market-data providers or external data dependencies.

    It never downloads quotes, filters symbols, calculates technical scores,
    ranks opportunities or makes trading decisions.
    """

    def create_sections(self, result: Any) -> list[GuiSection]:
        status = result.status
        opportunities = result.opportunities

        sections = [
            self._create_summary_section(status),
            self._create_pipeline_section(status),
            self._create_timing_section(status),
            self._create_opportunities_section(opportunities),
        ]

        diagnostics = self._create_diagnostics_section(status)
        if diagnostics is not None:
            sections.append(diagnostics)

        return sections

    def _create_summary_section(self, status: Any) -> GuiSection:
        return GuiSection(
            title="Scanner Summary",
            description="High-level scan status produced before the GUI receives the result.",
            metrics=[
                GuiMetric("Universe", str(getattr(status, "universe_count", 0))),
                GuiMetric("Quotes", str(getattr(status, "quotes_count", 0))),
                GuiMetric("Technical Results", str(getattr(status, "technical_results_count", 0))),
                GuiMetric("Opportunities", str(getattr(status, "opportunities_count", 0))),
            ],
        )

    def _create_pipeline_section(self, status: Any) -> GuiSection:
        return GuiSection(
            title="Scanner Pipeline",
            description="Deterministic funnel counts from the Scan Pipeline.",
            metrics=[
                GuiMetric("After Price Filter", str(getattr(status, "after_price_filter", 0))),
                GuiMetric("After Volume Filter", str(getattr(status, "after_volume_filter", 0))),
                GuiMetric("After Liquidity Filter", str(getattr(status, "after_liquidity_filter", 0))),
                GuiMetric("After Relative Strength", str(getattr(status, "after_relative_strength_filter", 0))),
                GuiMetric("After Momentum", str(getattr(status, "after_momentum_filter", 0))),
                GuiMetric("Technical Candidates", str(getattr(status, "technical_candidates_count", 0))),
            ],
        )

    def _create_timing_section(self, status: Any) -> GuiSection:
        return GuiSection(
            title="Scanner Runtime",
            description="Runtime measurements captured by the scanner layer.",
            metrics=[
                GuiMetric("Provider", getattr(status, "market_data_provider", "") or "N/A"),
                GuiMetric("Quote Seconds", f"{getattr(status, 'quote_seconds', 0.0):.4f}"),
                GuiMetric("Technical Scanner Seconds", f"{getattr(status, 'technical_scanner_seconds', 0.0):.4f}"),
                GuiMetric("Ranking Seconds", f"{getattr(status, 'ranking_seconds', 0.0):.4f}"),
                GuiMetric("Total Seconds", f"{getattr(status, 'total_seconds', 0.0):.4f}"),
            ],
        )

    def _create_opportunities_section(self, opportunities: list[Any]) -> GuiSection:
        if not opportunities:
            return GuiSection(
                title="Top Opportunities",
                description="No ranked opportunities were returned by the scanner.",
                metrics=[GuiMetric("Result", "None")],
            )

        metrics: list[GuiMetric] = []

        for index, opportunity in enumerate(opportunities, start=1):
            metrics.extend(
                [
                    GuiMetric(f"#{index} Symbol", getattr(opportunity, "symbol", "N/A")),
                    GuiMetric(f"#{index} Action", getattr(opportunity, "action", "N/A")),
                    GuiMetric(f"#{index} Confidence", f"{getattr(opportunity, 'confidence', 0.0):.2f}"),
                    GuiMetric(f"#{index} Reason", getattr(opportunity, "reason", "")),
                ]
            )

        return GuiSection(
            title="Top Opportunities",
            description="Ranked opportunities supplied by the deterministic Ranking Engine.",
            metrics=metrics,
        )

    def _create_diagnostics_section(self, status: Any) -> GuiSection | None:
        diagnostics: list[GuiMetric] = []

        quote_missing = getattr(status, "quote_missing", 0)
        provider_missing_quotes = getattr(status, "provider_missing_quotes", 0)
        messages = getattr(status, "messages", [])

        if quote_missing:
            diagnostics.append(GuiMetric("Missing Quotes", str(quote_missing)))

        if provider_missing_quotes:
            diagnostics.append(GuiMetric("Provider Missing Quotes", str(provider_missing_quotes)))

        for index, message in enumerate(messages, start=1):
            diagnostics.append(GuiMetric(f"Message {index}", message))

        if not diagnostics:
            return None

        return GuiSection(
            title="Scanner Diagnostics",
            description="Warnings and messages generated by the scanner layer.",
            metrics=diagnostics,
        )
