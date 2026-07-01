from typing import Any

from services.analysis.models import IndicatorResult
from ui.foundation.models import GuiMetric, GuiSection


class IndicatorPresenter:
    """
    Builds display-only indicator dashboard sections for the GUI.

    The presenter consumes deterministic IndicatorResult objects from the
    Indicator Engine and projects them into stable GUI sections. It never
    calculates indicators, interprets indicator values, generates signals or
    makes trading decisions.
    """

    def create_sections(self, indicator_result: IndicatorResult) -> list[GuiSection]:
        return [
            self._create_summary_section(indicator_result),
            self._create_trend_section(indicator_result),
            self._create_momentum_section(indicator_result),
            self._create_volatility_section(indicator_result),
            self._create_structure_volume_section(indicator_result),
        ]

    def _create_summary_section(self, indicator_result: IndicatorResult) -> GuiSection:
        return GuiSection(
            title="Indicator Dashboard",
            description="Display-only view of deterministic Indicator Engine output.",
            metrics=[
                GuiMetric("Symbol", indicator_result.symbol.upper() or "N/A"),
                GuiMetric("Indicator Count", str(len(indicator_result.values))),
                GuiMetric("Presentation Only", "Yes"),
            ],
        )

    def _create_trend_section(self, indicator_result: IndicatorResult) -> GuiSection:
        return GuiSection(
            title="Trend Indicators",
            description="Trend-related values calculated before the GUI receives the result.",
            metrics=[
                self._metric(indicator_result, "SMA20", "sma20"),
                self._metric(indicator_result, "SMA50", "sma50"),
                self._metric(indicator_result, "EMA20", "ema20"),
                self._metric(indicator_result, "EMA50", "ema50"),
                self._metric(indicator_result, "ADX14", "adx14"),
            ],
        )

    def _create_momentum_section(self, indicator_result: IndicatorResult) -> GuiSection:
        return GuiSection(
            title="Momentum Indicators",
            description="Momentum values produced by the Indicator Engine.",
            metrics=[
                self._metric(indicator_result, "RSI14", "rsi14"),
                self._metric(indicator_result, "MACD", "macd"),
            ],
        )

    def _create_volatility_section(self, indicator_result: IndicatorResult) -> GuiSection:
        return GuiSection(
            title="Volatility Indicators",
            description="Volatility values produced by the Indicator Engine.",
            metrics=[
                self._metric(indicator_result, "ATR14", "atr14"),
                self._metric(indicator_result, "Bollinger Bands", "bollinger"),
            ],
        )

    def _create_structure_volume_section(self, indicator_result: IndicatorResult) -> GuiSection:
        return GuiSection(
            title="Structure, Volume and Relative Strength",
            description="Supporting market structure, volume and benchmark-aware indicator values.",
            metrics=[
                self._metric(indicator_result, "Latest Close", "latest_close"),
                self._metric(indicator_result, "Recent High 20", "recent_high_20"),
                self._metric(indicator_result, "Recent Low 20", "recent_low_20"),
                self._metric(indicator_result, "Latest Volume", "latest_volume"),
                self._metric(indicator_result, "Average Volume 20", "average_volume_20"),
                self._metric(indicator_result, "Relative Volume 20", "relative_volume_20"),
                self._metric(indicator_result, "Relative Strength 20", "relative_strength_20"),
                self._metric(indicator_result, "Relative Strength 50", "relative_strength_50"),
            ],
        )

    def _metric(
        self,
        indicator_result: IndicatorResult,
        label: str,
        key: str,
    ) -> GuiMetric:
        return GuiMetric(label, self._format_value(indicator_result.get(key)))

    def _format_value(self, value: Any) -> str:
        if value is None:
            return "N/A"

        if isinstance(value, float):
            return f"{value:.4f}"

        if isinstance(value, int):
            return str(value)

        if isinstance(value, dict):
            if not value:
                return "N/A"
            formatted_items = [
                f"{key}={self._format_value(value[key])}"
                for key in sorted(value.keys())
            ]
            return ", ".join(formatted_items)

        if isinstance(value, (list, tuple)):
            if not value:
                return "N/A"
            return ", ".join(self._format_value(item) for item in value)

        return str(value)
