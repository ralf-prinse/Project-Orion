from typing import Any

from ui.foundation.models import GuiMetric, GuiSection


class UniversePresenter:
    """
    Builds display-only universe dashboard sections for the GUI.

    The presenter consumes symbol lists and optional update statistics that were
    already produced by the Universe Layer. It formats them for presentation
    only. It never downloads exchange files, reads universe files, normalizes
    symbols, filters tickers, scans stocks or performs trading logic.
    """

    def create_sections(
        self,
        symbols: list[str],
        update_stats: dict[str, Any] | None = None,
    ) -> list[GuiSection]:
        normalized_symbols = [str(symbol).upper() for symbol in symbols if str(symbol).strip()]
        return [
            self._create_summary_section(normalized_symbols, update_stats),
            self._create_symbol_preview_section(normalized_symbols),
            self._create_update_statistics_section(update_stats),
        ]

    def _create_summary_section(
        self,
        symbols: list[str],
        update_stats: dict[str, Any] | None,
    ) -> GuiSection:
        return GuiSection(
            title="Universe Dashboard",
            description="Display-only view of deterministic stock universe output.",
            metrics=[
                GuiMetric("Symbol Count", str(len(symbols))),
                GuiMetric("First Symbol", symbols[0] if symbols else "N/A"),
                GuiMetric("US Market Count", self._format_optional_stat(update_stats, "us_market")),
                GuiMetric("Presentation Only", "Yes"),
            ],
        )

    def _create_symbol_preview_section(self, symbols: list[str]) -> GuiSection:
        if not symbols:
            metrics = [GuiMetric("Symbols", "None")]
        else:
            preview_symbols = symbols[:10]
            metrics = [
                GuiMetric("Preview Count", str(len(preview_symbols))),
                GuiMetric("Symbols", ", ".join(preview_symbols)),
            ]

        return GuiSection(
            title="Universe Symbols",
            description="Preview of symbols supplied by the Universe Layer before reaching the GUI.",
            metrics=metrics,
        )

    def _create_update_statistics_section(self, update_stats: dict[str, Any] | None) -> GuiSection:
        if not update_stats:
            metrics = [GuiMetric("Update Statistics", "N/A")]
        else:
            metrics = [
                GuiMetric("NASDAQ Symbols", self._format_optional_stat(update_stats, "nasdaq")),
                GuiMetric("Other US Symbols", self._format_optional_stat(update_stats, "us_other")),
                GuiMetric("US Market Symbols", self._format_optional_stat(update_stats, "us_market")),
            ]

        return GuiSection(
            title="Universe Update Statistics",
            description="Universe counts produced outside the GUI layer.",
            metrics=metrics,
        )

    def _format_optional_stat(self, stats: dict[str, Any] | None, key: str) -> str:
        if not stats or key not in stats:
            return "N/A"
        return str(stats[key])
