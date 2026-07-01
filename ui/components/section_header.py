from dataclasses import dataclass

from ui.design import ORION_DARK_THEME, OrionTheme


@dataclass(frozen=True)
class SectionHeaderViewModel:
    title: str
    subtitle: str = ""
    action_label: str = ""


class SectionHeaderComponent:
    def __init__(self, theme: OrionTheme | None = None):
        self.theme = theme or ORION_DARK_THEME

    def create(self, title: str, subtitle: str = "", action_label: str = "") -> SectionHeaderViewModel:
        return SectionHeaderViewModel(
            title=title.strip(),
            subtitle=subtitle.strip(),
            action_label=action_label.strip(),
        )
