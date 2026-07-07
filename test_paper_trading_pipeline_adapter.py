from __future__ import annotations

import pandas as pd

from models.trading_pipeline_result import TradingPipelineResult
from services.paper_trading_pipeline_adapter import PaperTradingPipelineAdapter


class FakePortfolio:
    cash = 10000.0
    position_size = 0.0
    exposure = 0.0
    max_position_percentage = 1.0


def _build_history() -> pd.DataFrame:
    rows = []

    for index in range(60):
        close = 100 + index

        rows.append(
            {
                "Open": close - 0.5,
                "High": close + 1.0,
                "Low": close - 1.0,
                "Close": close,
                "Volume": 1000 + index,
            }
        )

    return pd.DataFrame(rows)


def main():
    adapter = PaperTradingPipelineAdapter()

    result = adapter.run(
        symbol="inga.as",
        history=_build_history(),
        portfolio_state=FakePortfolio(),
    )

    assert isinstance(result, TradingPipelineResult)
    assert result.symbol == "INGA.AS"
    assert result.decision in {"BUY", "HOLD", "SELL"}
    assert result.confidence >= 0
    assert result.position_size >= 0
    assert result.risk_plan.symbol == "INGA.AS"
    assert result.risk_plan.entry_price > 0
    assert result.legacy_output["symbol"] == "INGA.AS"

    print("PAPER TRADING PIPELINE ADAPTER: PASS ✅")


if __name__ == "__main__":
    main()