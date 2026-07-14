from __future__ import annotations

import math
from datetime import UTC, datetime

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.paper_position_update_service import (
    PaperPositionUpdateService,
)
from services.portfolio_revaluation_service import (
    PortfolioRevaluationService,
)


def build_risk_plan(
    symbol: str,
) -> RiskPlan:
    return RiskPlan(
        symbol=symbol,
        entry_price=100.0,
        stop_loss=95.0,
        target_1=105.0,
        target_2=110.0,
        target_3=115.0,
        risk_percent=5.0,
        reward_percent=15.0,
        risk_reward_ratio=3.0,
        confidence=0.85,
        notes="Quote-safety regression test.",
    )


def build_state(
    symbol: str,
) -> PositionState:
    return PositionState(
        symbol=symbol,
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=100.0,
        current_price=100.0,
        opened_at=datetime(
            2026,
            7,
            14,
            10,
            0,
            tzinfo=UTC,
        ),
    )


def build_session() -> TradingSession:
    positions = {
        "AAPL": PaperPosition(
            symbol="AAPL",
            quantity=2,
            entry_price=100.0,
            current_price=100.0,
        ),
        "MSFT": PaperPosition(
            symbol="MSFT",
            quantity=2,
            entry_price=100.0,
            current_price=100.0,
        ),
    }

    return TradingSession(
        name="Quote Safety Test",
        portfolio=PaperPortfolio(
            cash=600.0,
            positions=positions,
        ),
        position_states={
            "AAPL": build_state("AAPL"),
            "MSFT": build_state("MSFT"),
        },
        risk_plans={
            "AAPL": build_risk_plan("AAPL"),
            "MSFT": build_risk_plan("MSFT"),
        },
        status="ACTIVE",
    )


def test_position_update_rejects_nan_without_mutation():
    service = PaperPositionUpdateService()
    session = build_session()

    original_equity = session.equity
    original_state = (
        session.position_states["AAPL"]
    )
    original_position = (
        session.portfolio.positions["AAPL"]
    )

    result = service.update_position(
        session=session,
        symbol="AAPL",
        current_price=float("nan"),
    )

    assert result.updated is False
    assert result.session is session
    assert "Invalid quote ignored" in result.message

    assert (
        session.portfolio.positions["AAPL"]
        is original_position
    )
    assert (
        session.position_states["AAPL"]
        is original_state
    )
    assert session.equity == original_equity
    assert math.isfinite(session.equity)


def test_position_update_rejects_infinity():
    service = PaperPositionUpdateService()
    session = build_session()

    result = service.update_position(
        session=session,
        symbol="AAPL",
        current_price=float("inf"),
    )

    assert result.updated is False
    assert result.session.equity == 1000.0
    assert math.isfinite(result.session.equity)


def test_position_update_rejects_zero_and_negative():
    service = PaperPositionUpdateService()

    for invalid_price in (0, -1.0):
        session = build_session()

        result = service.update_position(
            session=session,
            symbol="AAPL",
            current_price=invalid_price,
        )

        assert result.updated is False
        assert (
            result.session
            .portfolio
            .positions["AAPL"]
            .current_price
            == 100.0
        )


def test_valid_position_update_still_works():
    service = PaperPositionUpdateService()
    session = build_session()

    result = service.update_position(
        session=session,
        symbol="AAPL",
        current_price=104.0,
    )

    assert result.updated is True
    assert (
        result.session
        .portfolio
        .positions["AAPL"]
        .current_price
        == 104.0
    )
    assert math.isfinite(
        result.session.equity
    )


def test_revaluation_skips_bad_symbol_and_updates_good_symbol():
    service = PortfolioRevaluationService()
    portfolio = build_session().portfolio

    result = service.revalue(
        portfolio=portfolio,
        prices={
            "AAPL": float("nan"),
            "MSFT": 110.0,
        },
    )

    assert (
        result.positions["AAPL"].current_price
        == 100.0
    )
    assert (
        result.positions["MSFT"].current_price
        == 110.0
    )

    assert result.equity == 1020.0
    assert math.isfinite(result.equity)


def test_revaluation_rejects_all_invalid_price_types():
    service = PortfolioRevaluationService()

    invalid_prices = (
        float("nan"),
        float("inf"),
        float("-inf"),
        0,
        -10.0,
        "unknown",
    )

    for invalid_price in invalid_prices:
        portfolio = build_session().portfolio

        result = service.revalue(
            portfolio=portfolio,
            prices={
                "AAPL": invalid_price,
            },
        )

        assert (
            result.positions["AAPL"]
            .current_price
            == 100.0
        )
        assert math.isfinite(result.equity)


def run():
    test_position_update_rejects_nan_without_mutation()
    test_position_update_rejects_infinity()
    test_position_update_rejects_zero_and_negative()
    test_valid_position_update_still_works()
    test_revaluation_skips_bad_symbol_and_updates_good_symbol()
    test_revaluation_rejects_all_invalid_price_types()

    print("QUOTE SAFETY PIPELINE: PASS")


if __name__ == "__main__":
    run()