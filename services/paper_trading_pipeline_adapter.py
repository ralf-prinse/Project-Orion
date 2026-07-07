from __future__ import annotations

import pandas as pd

from models.trading_pipeline_result import TradingPipelineResult
from services.intelligence.indicator_builder import IndicatorBuilder
from services.orchestration.trading_pipeline import TradingPipeline


class PaperTradingPipelineAdapter:
    """
    Adapter between market data and the TradingPipeline.

    Responsibilities
    ----------------
    - Convert historical OHLCV data into IndicatorPack
    - Run TradingPipeline
    - Return TradingPipelineResult

    Does NOT
    --------
    - Execute orders
    - Mutate portfolio
    - Communicate with broker
    - Generate decisions outside TradingPipeline
    """

    def __init__(
        self,
        indicator_builder: IndicatorBuilder | None = None,
        trading_pipeline: TradingPipeline | None = None,
    ):
        self.indicator_builder = indicator_builder or IndicatorBuilder()
        self.trading_pipeline = trading_pipeline or TradingPipeline()

    def run(
        self,
        symbol: str,
        history: pd.DataFrame,
        portfolio_state,
    ) -> TradingPipelineResult:
        normalized_symbol = str(symbol).strip().upper()

        if not normalized_symbol:
            raise ValueError("Symbol may not be empty.")

        if history is None or history.empty:
            raise ValueError("History may not be empty.")

        indicators = self.indicator_builder.build(
            symbol=normalized_symbol,
            history=history,
        )

        return self.trading_pipeline.run(
            indicator_data=indicators,
            portfolio_state=portfolio_state,
        )