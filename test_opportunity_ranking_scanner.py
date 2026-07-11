from pathlib import Path
import sys
import types
import pandas as pd

sys.modules.setdefault("yfinance", types.SimpleNamespace())
from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner


class FakeProvider:
    def get_historical_data(self, symbol, period="3mo", interval="1d"):
        rows=[]
        boost={"AAPL": 1.5, "MSFT": 1.0}.get(symbol, 0.5)
        for index in range(80):
            close=100 + index * boost
            rows.append({"Open":close-0.5,"High":close+1,"Low":close-1,"Close":close,"Volume":1000+index*10})
        return pd.DataFrame(rows)


def main():
    scanner=LivePaperMarketScanner(
        config=LivePaperTradingConfig(watchlist_path=Path("data/universes/swing.csv"), max_symbols=3),
        provider=FakeProvider(),
    )
    result=scanner.run()
    assert len(result.candidates)==3
    assert all(c.opportunity_ranking is not None for c in result.candidates)
    assert [c.score for c in result.ranked_candidates] == sorted([c.score for c in result.candidates], reverse=True)
    print("OPPORTUNITY RANKING SCANNER: PASS ✅")


if __name__ == "__main__":
    main()
