from dataclasses import dataclass, field
from typing import Any, List, Optional


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
class GuiWorkspace:
    """
    Canonical presentation model for a complete dashboard workspace.

    GuiWorkspace is used by presenters to deliver cards, charts and sections
    through one unified presentation pipeline.

    This model contains presentation data only.
    """

    title: str
    subtitle: str = ""
    cards: List[Any] = field(default_factory=list)
    charts: List[Any] = field(default_factory=list)
    sections: List[GuiWorkspaceSection] = field(default_factory=list)
    status: str = "neutral"
    metadata: Optional[dict] = None