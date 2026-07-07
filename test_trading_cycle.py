from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.trading_cycle import TradingCycle


def _pipeline_output(symbol: str, entry: float) -> dict:
    return {
        "symbol": symbol,
        "confidence": 0.91,
        "risk_plan": {
            "symbol": symbol,
            "entry_price": entry,
            "stop_loss": entry * 0.95,
            "target_1": entry * 1.10,
            "target_2": entry * 1.20,
            "target_3": entry * 1.30,
            "risk_percent": 5.0,
            "reward_percent": 10.0,
            "risk_reward_ratio": 2.0,
            "confidence": 0.91,
            "notes": "test",
        },
    }


def run():
    cycle = TradingCycle()

    session = TradingSession(
        name="Cycle Test",
        portfolio=PaperPortfolio(
            cash=1000.0,
        ),
    )

    print("========== OPEN ==========")

    result = cycle.run(
        session=session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
            pipeline_output=_pipeline_output("AAPL", 100.0),
        ),
        quantity=2,
    )

    print(result)

    assert result.action == "OPEN_POSITION"
    assert result.session.cash == 800.0
    assert "AAPL" in result.session.portfolio.positions

    print("========== UPDATE ==========")

    result = cycle.run(
        session=result.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=112.0,
        ),
        quantity=2,
    )

    print(result)

    assert result.action == "UPDATE_POSITION"
    assert result.session.portfolio.positions["AAPL"].current_price == 112.0
    assert result.session.equity == 1024.0

    print("========== CLOSE ==========")

    result = cycle.run(
        session=result.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
        ),
        quantity=2,
    )

    print(result)

    assert result.action == "CLOSE_POSITION"
    assert result.session.open_positions == 0
    assert result.session.cash == 1000.0

    print("PASS")


if __name__ == "__main__":
    run()