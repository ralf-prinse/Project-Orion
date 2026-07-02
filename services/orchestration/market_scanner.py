from typing import List, Dict, Any

from services.orchestration.trading_pipeline import TradingPipeline
from services.intelligence.intelligence_models import IndicatorPack


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
        assets: List[IndicatorPack],
        portfolio_state,
    ) -> Dict[str, Any]:

        pipeline_results = []

        for asset in assets:

            result = self.pipeline.run(asset, portfolio_state)

            pipeline = result["pipeline"]
            ai_context = result["ai_context"]
            explanation = result["explanation"]

            pipeline_results.append(
                {
                    "symbol": pipeline["symbol"],
                    "pipeline": pipeline,
                    "ai_context": ai_context,
                    "explanation": explanation,
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
            if item["pipeline"]["decision"] in ("BUY", "SELL")
            and item["pipeline"]["confidence"] >= 0.60
        ]

        return {
            "best_trade": ranked[0] if ranked else None,
            "ranked": ranked,
            "actionable_trades": actionable,
            "total_scanned": len(assets),
        }

    @staticmethod
    def _ranking_score(item: Dict[str, Any]) -> float:
        pipeline = item["pipeline"]

        return (
            pipeline["pressure_score"]
            * pipeline["confidence"]
            * pipeline["strength"]
            - pipeline["risk_score"]
        )