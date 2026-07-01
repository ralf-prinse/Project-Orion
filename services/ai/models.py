from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from core.explainability import ExplanationReport


class ExplanationAudience(Enum):
    """
    Doelgroep voor deterministische Orion-uitleg.
    """

    TRADER = "TRADER"
    TECHNICAL = "TECHNICAL"
    EXECUTIVE = "EXECUTIVE"


@dataclass(frozen=True)
class AIExplanationConfig:
    """
    Configuratie voor de AI Explanation Layer Foundation.

    Deze configuratie stuurt alleen presentatie en samenvatting. Zij verandert
    nooit de onderliggende tradingbeslissing, performance-meting of planning.
    """

    audience: ExplanationAudience = ExplanationAudience.TRADER
    language: str = "nl"
    include_warnings: bool = True
    include_reasons: bool = True
    max_bullets_per_section: int = 5


@dataclass
class AIExplanationContext:
    """
    Invoer voor de AI Explanation Layer.

    De laag gebruikt uitsluitend deterministische resultaten van eerdere Orion-
    lagen. Zij mag geen nieuwe investeringsbeslissing, positieomvang, risico-
    oordeel of handelsplan verzinnen.
    """

    symbol: str = ""
    decision_result: Any | None = None
    trade_plan_result: Any | None = None
    performance_result: Any | None = None
    explanation_report: ExplanationReport | None = None
    title: str = ""

    def resolved_symbol(self) -> str:
        explicit_symbol = str(self.symbol).strip().upper()
        if explicit_symbol:
            return explicit_symbol

        for source in [
            self.decision_result,
            self.trade_plan_result,
            self.performance_result,
        ]:
            if source is not None and hasattr(source, "symbol"):
                value = str(getattr(source, "symbol", "")).strip().upper()
                if value:
                    return value

        return "UNKNOWN"


@dataclass(frozen=True)
class AIExplanationSection:
    """
    Eén gestructureerde uitlegsectie voor GUI, rapportage en toekomstige LLM-
    samenvattingen.
    """

    title: str
    bullets: list[str] = field(default_factory=list)


@dataclass
class AIExplanationResult:
    """
    Deterministische output van de AI Explanation Layer.

    Ondanks de naam voert deze foundation geen externe AI-call uit. Het resultaat
    is een gecontroleerde, reproduceerbare tekstuele uitleg die later veilig aan
    een LLM kan worden aangeboden als bronmateriaal.
    """

    symbol: str = ""
    title: str = ""
    valid_explanation: bool = False
    summary: str = ""
    sections: list[AIExplanationSection] = field(default_factory=list)
    source_count: int = 0
    warnings: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def add_section(self, title: str, bullets: list[str]) -> None:
        clean_bullets = [bullet for bullet in bullets if str(bullet).strip()]
        if clean_bullets:
            self.sections.append(AIExplanationSection(title=title, bullets=clean_bullets))

    def add_warning(self, warning: str) -> None:
        if warning:
            self.warnings.append(warning)

    def add_reason(self, reason: str) -> None:
        if reason:
            self.reasons.append(reason)
