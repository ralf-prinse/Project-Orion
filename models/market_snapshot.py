from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.trading_pipeline_result import TradingPipelineResult


@dataclass(frozen=True)
class MarketSnapshot:
    """
    One deterministic market update for one symbol.

    No trading decisions.
    No AI.

    Sprint 6E:
    - `pipeline_result` is the preferred typed interface.
    - `pipeline_output` remains temporarily available for legacy tests
      and backwards-compatible TradingCycle usage.
    """

    symbol: str
    current_price: float
    pipeline_result: TradingPipelineResult | None = None
    pipeline_output: dict[str, Any] | None = None

    @property
    def resolved_pipeline_output(
        self,
    ) -> TradingPipelineResult | dict[str, Any] | None:
        """
        Returns the preferred pipeline input for downstream paper trading.

        TradingPipelineResult has priority over legacy dictionary output.
        """
        if self.pipeline_result is not None:
            return self.pipeline_result

        return self.pipeline_output