from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.trading_cycle import TradingCycle


def build_pipeline_output() -> dict:
    return {
        "symbol": "AAPL",
        "confidence": 0.91,
        "risk_plan": {
            "symbol": "AAPL",
            "entry_price": 100.0,
            "stop_loss": 95.0,
            "target_1": 110.0,
            "target_2": 120.0,
            "target_3": 130.0,
            "risk_percent": 5.0,
            "reward_percent": 30.0,
            "risk_reward_ratio": 6.0,
            "confidence": 0.91,
            "notes": "TradingSession lifecycle ownership test.",
        },
    }


def test_trading_session_owns_full_lifecycle():
    cycle = TradingCycle()

    session = TradingSession(
        name="TradingSession Ownership Test",
        portfolio=PaperPortfolio(cash=1000.0),
    )

    opened = cycle.run(
        session=session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
            pipeline_output=build_pipeline_output(),
        ),
        quantity=2,
    )

    assert "AAPL" in opened.session.portfolio.positions
    assert "AAPL" in opened.session.position_states
    assert "AAPL" in opened.session.risk_plans

    updated = cycle.run(
        session=opened.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=112.0,
        ),
    )

    state = updated.session.position_states["AAPL"]
    assert state.current_price == 112.0
    assert state.highest_price == 112.0
    assert state.target_1_hit is True
    assert state.break_even_active is True
    assert state.trailing_stop_active is True

    closed = cycle.run(
        session=updated.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=106.0,
        ),
    )

    assert closed.action == "CLOSE_POSITION"
    assert closed.session.portfolio.positions == {}
    assert closed.session.position_states == {}
    assert closed.session.risk_plans == {}


def main():
    test_trading_session_owns_full_lifecycle()
    print("TRADING SESSION LIFECYCLE OWNERSHIP: PASS")


if __name__ == "__main__":
    main()
