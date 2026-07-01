from dataclasses import dataclass, field

from ui.components.card import CardViewModel


@dataclass(frozen=True)
class PanelViewModel:
    title: str
    cards: list[CardViewModel] = field(default_factory=list)
    description: str = ""


class PanelComponent:
    def create(
        self,
        title: str,
        cards: list[CardViewModel] | None = None,
        description: str = "",
    ) -> PanelViewModel:
        return PanelViewModel(
            title=title.strip(),
            cards=cards or [],
            description=description.strip(),
        )
