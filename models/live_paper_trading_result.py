from __future__ import annotations

from dataclasses import dataclass

from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession


@dataclass(frozen=True)
class LivePaperCandidate:
    symbol: str
    result: TradingPipelineResult
    score: float
    accepted: bool
    reason: str


@dataclass(frozen=True)
class LivePaperTradingResult:
    """
    Immutable result of one live paper trading scan.
    """

    session: TradingSession

    scanned_symbols: int
    failed_symbols: int

    candidates: list[LivePaperCandidate]

    executed_trades: int
    rejected_trades: int

    @property
    def ranked_candidates(self) -> list[LivePaperCandidate]:
        return sorted(
            self.candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

    @property
    def best_candidate(self) -> LivePaperCandidate | None:
        ranked = self.ranked_candidates

        if not ranked:
            return None

        return ranked[0]