from __future__ import annotations

import pandas as pd

from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from services.paper_trading_pipeline_adapter import PaperTradingPipelineAdapter
from services.trading_cycle import TradingCycle


class FakePortfolioState:
    cash = 10000.0
    position_size = 0.0
    exposure = 0.0
    max_position_percentage = 1.0


def _build_history() -> pd.DataFrame:
    rows = []

    for index in range(80):
        close = 100.0 + index

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
    print("\n=========================================")
    print("ORION TYPED PAPER TRADING FLOW TEST")
    print("=========================================\n")

    history = _build_history()

    adapter = PaperTradingPipelineAdapter()

    pipeline_result = adapter.run(
        symbol="inga.as",
        history=history,
        portfolio_state=FakePortfolioState(),
    )

    assert isinstance(pipeline_result, TradingPipelineResult)
    assert pipeline_result.symbol == "INGA.AS"
    assert pipeline_result.risk_plan.symbol == "INGA.AS"
    assert pipeline_result.risk_plan.entry_price > 0

    session = TradingSession(
        name="Typed Flow Test",
        portfolio=PaperPortfolio(
            cash=10000.0,
        ),
    )

    snapshot = MarketSnapshot(
        symbol="INGA.AS",
        current_price=float(history["Close"].iloc[-1]),
        pipeline_result=pipeline_result,
    )

    cycle = TradingCycle()

    result = cycle.run(
        session=session,
        snapshot=snapshot,
        quantity=1,
    )

    assert result.symbol == "INGA.AS"
    assert result.action in {"OPEN_POSITION", "OPEN_REJECTED"}

    if result.action == "OPEN_POSITION":
        assert "INGA.AS" in result.session.portfolio.positions
        assert "INGA.AS" in result.session.position_states
        assert "INGA.AS" in result.session.risk_plans
        assert result.session.cash < session.cash

    if result.action == "OPEN_REJECTED":
        assert result.opened is not None
        assert result.opened.executed is False
        assert result.session.cash == session.cash

    print("TYPED PAPER TRADING FLOW: PASS ✅")


if __name__ == "__main__":
    main()