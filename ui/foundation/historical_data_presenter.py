from typing import Any

from services.market_data.historical_provider import HistoricalProviderStats
from ui.foundation.models import GuiMetric, GuiSection


class HistoricalDataPresenter:
    """
    Builds display-only historical data dashboard sections for the GUI.

    The presenter consumes historical candle datasets that were already retrieved
    and validated by the Historical Data Layer. It formats metadata and latest
    candle values for presentation only. It never downloads candles, reads cache
    files, validates providers, calculates indicators, generates signals or makes
    trading decisions.
    """

    def create_sections(
        self,
        histories: dict[str, Any],
        stats: HistoricalProviderStats | None = None,
    ) -> list[GuiSection]:
        return [
            self._create_summary_section(histories, stats),
            self._create_dataset_section(histories),
            self._create_statistics_section(stats),
        ]

    def _create_summary_section(
        self,
        histories: dict[str, Any],
        stats: HistoricalProviderStats | None,
    ) -> GuiSection:
        symbols = [symbol.upper() for symbol in histories.keys()]
        return GuiSection(
            title="Historical Data Dashboard",
            description="Display-only view of deterministic historical candle data output.",
            metrics=[
                GuiMetric("Dataset Count", str(len(histories))),
                GuiMetric("Symbols", ", ".join(symbols) if symbols else "None"),
                GuiMetric("Requested Symbols", str(stats.requested_symbols) if stats else "N/A"),
                GuiMetric("Presentation Only", "Yes"),
            ],
        )

    def _create_dataset_section(self, histories: dict[str, Any]) -> GuiSection:
        metrics: list[GuiMetric] = []

        for symbol in sorted(histories.keys(), key=lambda item: item.upper()):
            dataset = histories[symbol]
            candle_count = self._get_candle_count(dataset)
            latest_close = self._get_latest_value(dataset, "Close")
            latest_volume = self._get_latest_value(dataset, "Volume")

            metrics.extend(
                [
                    GuiMetric(f"{symbol.upper()} Candles", str(candle_count)),
                    GuiMetric(f"{symbol.upper()} Latest Close", self._format_optional_money(latest_close)),
                    GuiMetric(f"{symbol.upper()} Latest Volume", self._format_optional_int(latest_volume)),
                ]
            )

        if not metrics:
            metrics.append(GuiMetric("Historical Datasets", "None"))

        return GuiSection(
            title="Historical Datasets",
            description="Latest historical candle metadata supplied before reaching the GUI.",
            metrics=metrics,
        )

    def _create_statistics_section(self, stats: HistoricalProviderStats | None) -> GuiSection:
        if stats is None:
            metrics = [GuiMetric("Statistics", "N/A")]
        else:
            metrics = [
                GuiMetric("Provider", stats.provider_name or "N/A"),
                GuiMetric("Requested Symbols", str(stats.requested_symbols)),
                GuiMetric("Received Symbols", str(stats.received_symbols)),
                GuiMetric("Missing Symbols", str(stats.missing_symbols)),
                GuiMetric("Cache Hits", str(stats.cache_hits)),
                GuiMetric("Fresh Downloads", str(stats.fresh_downloads)),
                GuiMetric("Duration Seconds", f"{stats.duration_seconds:.2f}"),
            ]

        return GuiSection(
            title="Historical Provider Statistics",
            description="Operational statistics produced outside the GUI layer.",
            metrics=metrics,
        )

    def _get_candle_count(self, dataset: Any) -> int:
        if dataset is None:
            return 0
        if hasattr(dataset, "empty") and dataset.empty:
            return 0
        try:
            return len(dataset)
        except TypeError:
            return 0

    def _get_latest_value(self, dataset: Any, column_name: str) -> float | int | None:
        if dataset is None or not hasattr(dataset, "columns"):
            return None
        if hasattr(dataset, "empty") and dataset.empty:
            return None

        columns_by_lower_name = {str(column).lower(): column for column in dataset.columns}
        column = columns_by_lower_name.get(column_name.lower())
        if column is None:
            return None

        try:
            value = dataset[column].iloc[-1]
        except Exception:
            return None

        if value is None:
            return None

        try:
            if value != value:
                return None
        except Exception:
            return None

        return value

    def _format_optional_money(self, value: float | int | None) -> str:
        if value is None:
            return "N/A"
        return f"${float(value):.2f}"

    def _format_optional_int(self, value: float | int | None) -> str:
        if value is None:
            return "N/A"
        return f"{int(value):,}"
