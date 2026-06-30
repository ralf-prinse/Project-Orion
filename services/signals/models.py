from dataclasses import dataclass, field
from enum import Enum


class Signal(Enum):
    """
    Mogelijke deterministische handelssignalen binnen Project Orion.
    """

    BUY = "BUY"
    WATCH = "WATCH"
    HOLD = "HOLD"
    SELL = "SELL"
    IGNORE = "IGNORE"


@dataclass
class SignalResult:
    """
    Resultaat van de Signal Layer.

    SignalResult bevat uitsluitend signaalinformatie.
    De daadwerkelijke investeringsbeslissing blijft de verantwoordelijkheid
    van de toekomstige Decision Engine.
    """

    symbol: str

    signal: Signal = Signal.IGNORE
    confidence: int = 0

    bullish_score: int = 0
    bearish_score: int = 0
    neutral_score: int = 0

    notes: list[str] = field(default_factory=list)

    def add_note(self, note: str):
        self.notes.append(note)