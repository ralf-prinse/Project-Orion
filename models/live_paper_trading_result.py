from __future__ import annotations

from dataclasses import dataclass

from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from models.opportunity_ranking import OpportunityRanking
from models.news_assessment import NewsAssessment


@dataclass(frozen=True)
class LivePaperCandidate:
    symbol: str
    result: TradingPipelineResult
    score: float
    accepted: bool
    reason: str
    opportunity_ranking: OpportunityRanking | None = None
    news_assessment: NewsAssessment | None = None


@dataclass(frozen=True)
class LivePaperTradingResult:
    """
    Immutable result of one live paper trading scan.
    """

    session: TradingSession

    scanned_symbols: int
    succeeded_symbols: int
    failed_symbols: int
    failed_symbol_errors: dict[str, str]
    scan_duration_seconds: float

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
