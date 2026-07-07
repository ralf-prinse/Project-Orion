from __future__ import annotations

import pandas as pd

from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.paper_trading_demo_result import PaperTradingDemoResult
from models.trading_session import TradingSession
from services.paper_trading_pipeline_adapter import PaperTradingPipelineAdapter
from services.paper_trading_runner import PaperTradingRunner


class DemoPortfolioState:
    cash = 10000.0
    position_size = 0.0
    exposure = 0.0
    max_position_percentage = 1.0


class PaperTradingDemoRunner:
    """
    Deterministic demo runner for Orion paper trading.

    This runner uses synthetic market data so the demo is stable,
    repeatable and independent from external APIs.
    """

    def __init__(
        self,
        adapter: PaperTradingPipelineAdapter | None = None,
        runner: PaperTradingRunner | None = None,
    ):
        self.adapter = adapter or PaperTradingPipelineAdapter()
        self.runner = runner or PaperTradingRunner()

    def run(
        self,
        symbol: str = "INGA.AS",
        initial_cash: float = 10000.0,
        quantity: int = 1,
    ) -> PaperTradingDemoResult:
        normalized_symbol = symbol.strip().upper()

        history = self._build_demo_history()

        pipeline_result = self.adapter.run(
            symbol=normalized_symbol,
            history=history,
            portfolio_state=DemoPortfolioState(),
        )

        snapshots = [
            MarketSnapshot(
                symbol=normalized_symbol,
                current_price=float(history["Close"].iloc[-1]),
                pipeline_result=pipeline_result,
            ),
            MarketSnapshot(
                symbol=normalized_symbol,
                current_price=float(history["Close"].iloc[-1]) * 1.01,
            ),
            MarketSnapshot(
                symbol=normalized_symbol,
                current_price=float(history["Close"].iloc[-1]) * 1.02,
            ),
        ]

        session = TradingSession(
            name="Orion Paper Trading Demo",
            portfolio=PaperPortfolio(
                cash=initial_cash,
            ),
        )

        run_result = self.runner.run(
            session=session,
            snapshots=snapshots,
            quantity=quantity,
        )

        return PaperTradingDemoResult(
            run=run_result,
            initial_cash=initial_cash,
            final_cash=run_result.session.cash,
            final_equity=run_result.session.equity,
            total_cycles=run_result.total_cycles,
            opened_positions=run_result.opened_positions,
            closed_positions=run_result.closed_positions,
        )

    def _build_demo_history(
        self,
    ) -> pd.DataFrame:
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