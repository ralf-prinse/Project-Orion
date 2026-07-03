from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ui.foundation.chart_models import (
    GuiAxis,
    GuiChartType,
    GuiLegend,
    GuiSeries,
)


@dataclass(frozen=True)
class GuiChart:
    """
    Presentation-only chart model.

    GuiChart describes chart data for the desktop presentation layer.
    It contains no business logic and performs no calculations.
    """

    title: str
    chart_type: GuiChartType
    series: list[GuiSeries] = field(default_factory=list)
    subtitle: str = ""
    x_axis: GuiAxis = field(default_factory=GuiAxis)
    y_axis: GuiAxis = field(default_factory=GuiAxis)
    legend: GuiLegend = field(default_factory=GuiLegend)
    status: str = "neutral"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuiChartSection:
    """
    Presentation-only grouping model for related charts.
    """

    title: str
    charts: list[GuiChart] = field(default_factory=list)
    subtitle: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)