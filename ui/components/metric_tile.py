from dataclasses import dataclass

from ui.design import ORION_DARK_THEME, OrionTheme


@dataclass(frozen=True)
class MetricTileViewModel:
    label: str
    value: str
    helper_text: str = ""
    trend: str = "neutral"


class MetricTileComponent:
    def __init__(self, theme: OrionTheme | None = None):
        self.theme = theme or ORION_DARK_THEME

    def create(
        self,
        label: str,
        value: object,
        helper_text: str = "",
        trend: str = "neutral",
    ) -> MetricTileViewModel:
        return MetricTileViewModel(
            label=label.strip(),
            value=str(value),
            helper_text=helper_text.strip(),
            trend=trend.strip().lower() or "neutral",
        )
