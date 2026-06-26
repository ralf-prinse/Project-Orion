from dataclasses import dataclass

from services.scanner.technical_scanner import TechnicalScanResult


@dataclass
class RankedOpportunity:
    symbol: str
    action: str
    confidence: float
    reason: str


class RankingEngine:
    """
    Rangschikt scanresultaten tot concrete koopkansen.

    Belangrijk:
    - IGNORE-resultaten worden niet getoond als koopkans.
    - BUY komt boven HOLD.
    - Binnen dezelfde actie sorteert Orion op confidence.
    """

    ACTION_PRIORITY = {
        "BUY": 3,
        "HOLD": 2,
        "IGNORE": 1,
    }

    def rank(
        self,
        results: list[TechnicalScanResult],
        limit: int = 3,
    ) -> list[RankedOpportunity]:
        actionable_results = [
            result
            for result in results
            if result.signal in {"BUY", "HOLD"}
        ]

        sorted_results = sorted(
            actionable_results,
            key=lambda result: (
                self.ACTION_PRIORITY.get(result.signal, 0),
                result.technical_score,
            ),
            reverse=True,
        )

        opportunities: list[RankedOpportunity] = []

        for result in sorted_results[:limit]:
            opportunities.append(
                RankedOpportunity(
                    symbol=result.symbol,
                    action=result.signal,
                    confidence=result.technical_score,
                    reason=result.reason,
                )
            )

        return opportunities