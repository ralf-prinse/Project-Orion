from dataclasses import dataclass, field

from ui.design import ORION_DARK_THEME, OrionTheme
from ui.foundation.models import GuiMetric


@dataclass(frozen=True)
class CardViewModel:
    """
    Toolkit-independent card model.

    Real Qt widgets can render this model later. Keeping the first component
    layer data-only preserves testability and prevents trading logic from
    entering the GUI.
    """

    title: str
    description: str = ""
    metrics: list[GuiMetric] = field(default_factory=list)
    accent: str = "neutral"


class CardComponent:
    def __init__(self, theme: OrionTheme | None = None):
        self.theme = theme or ORION_DARK_THEME

    def create(
        self,
        title: str,
        description: str = "",
        metrics: list[GuiMetric] | None = None,
        accent: str = "neutral",
    ) -> CardViewModel:
        return CardViewModel(
            title=title.strip(),
            description=description.strip(),
            metrics=metrics or [],
            accent=accent.strip().lower() or "neutral",
        )

    def stylesheet(self) -> str:
        return self.theme.card_style()
