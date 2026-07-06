from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from models.portfolio import Portfolio
from services.orchestration.market_pipeline_scanner_service import (
    MarketPipelineScannerService,
)


class FakeWatchlistService:
    def load_symbols(self) -> list[str]:
        return ["AAPL", "ASML.AS"]


class FakeHistoricalProvider:
    def get_history(
        self,
        symbols: list[str],
        period: str = "6mo",
        interval: str = "1d",
    ) -> dict[str, pd.DataFrame]:
        return {
            symbol: self._history()
            for symbol in symbols
        }

    def _history(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Close": [100.0, 101.0, 102.0],
                "Volume": [1000, 1100, 1200],
            }
        )


@dataclass
class FakeIndicatorPack:
    symbol: str


class FakeIndicatorBuilder:
    def build(
        self,
        symbol: str,
        history: pd.DataFrame,
    ) -> FakeIndicatorPack:
        return FakeIndicatorPack(symbol=symbol)


class FakeTradingPipeline:
    def run(
        self,
        indicator_data,
        portfolio_state,
    ) -> dict:
        decision = "BUY" if indicator_data.symbol == "AAPL" else "HOLD"

        return {
            "pipeline": {
                "symbol": indicator_data.symbol,
                "decision": decision,
                "confidence": 0.91 if decision == "BUY" else 0.55,
                "position_size": 500.0 if decision == "BUY" else 0.0,
                "expected_risk": 0.05,
                "reason": "Test pipeline decision",
            },
            "ai_context": None,
            "explanation": {
                "summary": "Test explanation",
                "details": [],
            },
        }


def main():
    scanner = MarketPipelineScannerService(
        watchlist_service=FakeWatchlistService(),
        historical_provider=FakeHistoricalProvider(),
        indicator_builder=FakeIndicatorBuilder(),
        trading_pipeline=FakeTradingPipeline(),
    )

    portfolio = Portfolio(
        cash=1000.0,
        currency="EUR",
        max_position_percentage=1.0,
    )

    snapshot = scanner.scan(portfolio_state=portfolio)

    assert snapshot.total_symbols == 2
    assert snapshot.total_results == 2
    assert not snapshot.has_errors

    assert len(snapshot.buy_results) == 1
    assert snapshot.buy_results[0].symbol == "AAPL"
    assert snapshot.buy_results[0].decision == "BUY"
    assert snapshot.buy_results[0].confidence == 0.91
    assert snapshot.buy_results[0].position_size == 500.0

    assert snapshot.top_buy_results[0].symbol == "AAPL"

    print("MARKET PIPELINE SCANNER SERVICE: PASS ✅")


if __name__ == "__main__":
    main()