from dataclasses import dataclass, field
from typing import Any


@dataclass
class IndicatorResult:
    """
    Bevat alle berekende indicatoren voor één aandeel.

    De Indicator Engine vult dit object.
    De Analysis Engine leest dit object.
    """

    symbol: str

    values: dict[str, Any] = field(default_factory=dict)

    def set(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: str, default=None):
        return self.values.get(name, default)

    def has(self, name: str):
        return name in self.values


@dataclass
class AnalysisResult:
    """
    Resultaat van de volledige technische analyse.
    """

    symbol: str

    trend_score: int = 0
    momentum_score: int = 0
    volatility_score: int = 0
    structure_score: int = 0
    volume_score: int = 0
    market_regime_score: int = 0
    relative_strength_score: int = 0

    overall_score: int = 0

    notes: list[str] = field(default_factory=list)

    def add_note(self, note: str):
        self.notes.append(note)