from dataclasses import dataclass
from enum import Enum
from typing import Any


class ExplanationSeverity(Enum):
    """
    Ernstniveau van een explainability-item.
    """

    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKER = "BLOCKER"


@dataclass(frozen=True)
class ExplanationItem:
    """
    Eén gestructureerde verklaring binnen Project Orion.
    """

    code: str
    category: str
    severity: ExplanationSeverity
    title: str
    message: str

    current_value: Any | None = None
    threshold: Any | None = None
    passed: bool | None = None