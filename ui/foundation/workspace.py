from dataclasses import dataclass, field
from typing import Any, List, Optional

from ui.foundation.charts import GuiChart, GuiChartSection


@dataclass(frozen=True)
class GuiWorkspaceSection:
    """
    Presentation-only section model for dashboard workspaces.

    A section groups related dashboard presentation items.
    It contains no business logic and performs no calculations.
    """

    title: str
    subtitle: str = ""
    items: List[Any] = field(default_factory=list)


@dataclass(frozen=True)
class GuiWorkspacePanel:
    """
    Presentation-only panel model.

    Panels allow Orion workspaces to display specialized UI blocks such as:
    - live scanner output
    - open positions
    - alerts
    - news
    - broker status

    The panel contains prepared presentation data only.
    """

    panel_type: str
    title: str = ""
    subtitle: str = ""
    items: List[Any] = field(default_factory=list)
    status: str = "neutral"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuiWorkspace:
    """
    Canonical presentation model for a complete dashboard workspace.

    GuiWorkspace is used by presenters to deliver cards, panels, charts
    and sections through one unified presentation pipeline.

    This model contains presentation data only.
    """

    title: str
    subtitle: str = ""
    cards: List[Any] = field(default_factory=list)
    panels: List[GuiWorkspacePanel] = field(default_factory=list)
    charts: List[GuiChart] = field(default_factory=list)
    chart_sections: List[GuiChartSection] = field(default_factory=list)
    sections: List[GuiWorkspaceSection] = field(default_factory=list)
    status: str = "neutral"
    metadata: Optional[dict] = None