from dataclasses import dataclass

from ui.design import ORION_DARK_THEME, ORION_ICONS, OrionIcons, OrionTheme
from ui.foundation.models import GuiNavigationItem, GuiPage


@dataclass(frozen=True)
class SidebarButtonViewModel:
    page: GuiPage
    label: str
    icon: str
    enabled: bool
    selected: bool = False


class SidebarComponent:
    def __init__(
        self,
        theme: OrionTheme | None = None,
        icons: OrionIcons | None = None,
    ):
        self.theme = theme or ORION_DARK_THEME
        self.icons = icons or ORION_ICONS

    def create_buttons(
        self,
        items: list[GuiNavigationItem],
        current_page: GuiPage,
    ) -> list[SidebarButtonViewModel]:
        return [
            SidebarButtonViewModel(
                page=item.page,
                label=item.label,
                icon=self.icons.for_page(item.page),
                enabled=item.enabled,
                selected=item.page == current_page,
            )
            for item in sorted(items, key=lambda item: item.order)
        ]
