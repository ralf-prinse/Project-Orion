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


def test_trading_cycle_open_update_close():
    cycle = TradingCycle()

    assert not hasattr(
        cycle.paper_trading_service,
        "portfolio_repository",
    )

    session = TradingSession(
        name="Cycle Test",
        portfolio=PaperPortfolio(
            cash=1000.0,
        ),
    )

    open_result = cycle.run(
        session=session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
            pipeline_output=_pipeline_output(
                "AAPL",
                100.0,
            ),
        ),
        quantity=2,
    )

    assert open_result.action == "OPEN_POSITION"
    assert open_result.session.cash == 800.0
    assert "AAPL" in open_result.session.portfolio.positions
    assert "AAPL" in open_result.session.position_states
    assert "AAPL" in open_result.session.risk_plans

    update_result = cycle.run(
        session=open_result.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=112.0,
        ),
        quantity=2,
    )

    assert update_result.action == "UPDATE_POSITION"
    assert (
        update_result
        .session
        .portfolio
        .positions["AAPL"]
        .current_price
        == 112.0
    )
    assert update_result.session.equity == 1024.0

    close_result = cycle.run(
        session=update_result.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
        ),
        quantity=2,
    )

    assert close_result.action == "CLOSE_POSITION"
    assert close_result.session.open_positions == 0
    assert close_result.session.cash == 1000.0
    assert close_result.session.position_states == {}
    assert close_result.session.risk_plans == {}


def main():
    print()
    print("=========================================")
    print("TRADING CYCLE CONSOLIDATION TEST")
    print("=========================================")
    print()

    test_trading_cycle_open_update_close()

    print("TRADING CYCLE: PASS")


if __name__ == "__main__":
    main()
