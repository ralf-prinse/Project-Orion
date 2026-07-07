from typing import Any

from models.trading_pipeline_result import TradingPipelineResult
from services.intelligence.intelligence_models import IndicatorPack
from services.orchestration.trading_pipeline import TradingPipeline


class MarketScanner:
    """
    Runs the Orion trading pipeline for multiple assets
    and ranks the resulting trade opportunities.

    This class is responsible only for orchestration.
    It does not perform trading calculations itself.
    """

    def __init__(self):
        self.pipeline = TradingPipeline()

    def scan(
        self,
        assets: list[IndicatorPack],
        portfolio_state,
    ) -> dict[str, Any]:

        pipeline_results: list[dict[str, Any]] = []

        for asset in assets:
            result = self.pipeline.run(
                asset,
                portfolio_state,
            )

            pipeline_results.append(
                {
                    "symbol": result.symbol,
                    "pipeline": result,
                    "ai_context": result.ai_context,
                    "explanation": result.explanation,
                }
            )

        ranked = sorted(
            pipeline_results,
            key=self._ranking_score,
            reverse=True,
        )

        actionable = [
            item
            for item in ranked
            if item["pipeline"].decision in ("BUY", "SELL")
            and item["pipeline"].confidence >= 0.60
        ]

        return {
            "best_trade": ranked[0] if ranked else None,
            "ranked": ranked,
            "actionable_trades": actionable,
            "total_scanned": len(assets),
        }

    @staticmethod
    def _ranking_score(item: dict[str, Any]) -> float:
        pipeline: TradingPipelineResult = item["pipeline"]

        return (
            pipeline.confidence
            * pipeline.position_size
            - pipeline.expected_risk
        )