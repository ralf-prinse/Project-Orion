from dataclasses import dataclass, field

from core.explainability.explanation_item import (
    ExplanationItem,
    ExplanationSeverity,
)


@dataclass
class ExplanationReport:
    """
    Verzameling van gestructureerde explainability-items.
    """

    items: list[ExplanationItem] = field(default_factory=list)

    def add_item(
        self,
        item: ExplanationItem,
    ) -> None:
        self.items.append(item)

    def infos(self) -> list[ExplanationItem]:
        return [
            item
            for item in self.items
            if item.severity == ExplanationSeverity.INFO
        ]

    def warnings(self) -> list[ExplanationItem]:
        return [
            item
            for item in self.items
            if item.severity == ExplanationSeverity.WARNING
        ]

    def blockers(self) -> list[ExplanationItem]:
        return [
            item
            for item in self.items
            if item.severity == ExplanationSeverity.BLOCKER
        ]

    def has_blockers(self) -> bool:
        return len(self.blockers()) > 0