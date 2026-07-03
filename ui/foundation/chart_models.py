from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class GuiChartType(str, Enum):
    """
    Supported presentation chart types.

    Presentation-only.
    """

    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    DONUT = "donut"
    AREA = "area"


@dataclass(frozen=True)
class GuiAxis:
    """
    Presentation-only axis metadata.
    """

    label: str = ""
    unit: str = ""


@dataclass(frozen=True)
class GuiLegend:
    """
    Presentation-only legend configuration.
    """

    visible: bool = True
    position: str = "bottom"


@dataclass(frozen=True)
class GuiSeries:
    """
    Presentation-only chart data series.
    """

    name: str
    values: list[Any] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)