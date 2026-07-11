from __future__ import annotations

import json
from pathlib import Path

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.serialization.dataclass_serializer import (
    DataclassSerializer,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)
from services.trading_session_integrity_service import (
    TradingSessionIntegrityError,
    TradingSessionIntegrityService,
)


TEST_PATH = Path(
    "output/test_session_integrity.json"
)


def build_position() -> PaperPosition:
    return PaperPosition(
        symbol="AAPL",
        quantity=1,
        entry_price=100.0,
        current_price=106.0,
    )


def build_state() -> PositionState:
    return PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=100.7,
        highest_price=106.0,
        current_price=106.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=False,
        target_3_hit=False,
    )


def build_risk_plan() -> RiskPlan:
    return RiskPlan(
        symbol="AAPL",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=104.0,
        target_2=112.0,
        target_3=120.0,
        risk_percent=5.0,
        reward_percent=20.0,
        risk_reward_ratio=4.0,
        confidence=0.90,
        notes="Session integrity regression test.",
    )


def build_managed_session() -> TradingSession:
    return TradingSession(
        name="Managed Session",
        portfolio=PaperPortfolio(
            cash=400.0,
            positions={
                "AAPL": build_position(),
            },
        ),
        position_states={
            "AAPL": build_state(),
        },
        risk_plans={
            "AAPL": build_risk_plan(),
        },
        status="ACTIVE",
    )


def test_complete_managed_session_is_valid():
    service = TradingSessionIntegrityService()

    result = service.audit(
        build_managed_session()
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.managed_symbols == ("AAPL",)
    assert result.legacy_symbols == ()


def test_legacy_position_without_lifecycle_is_allowed():
    service = TradingSessionIntegrityService()

    session = TradingSession(
        name="Legacy Session",
        portfolio=PaperPortfolio(
            cash=400.0,
            positions={
                "AAPL": build_position(),
            },
        ),
        status="ACTIVE",
    )

    result = service.audit(session)

    assert result.valid is True
    assert result.managed_symbols == ()
    assert result.legacy_symbols == ("AAPL",)


def test_half_managed_position_is_rejected():
    service = TradingSessionIntegrityService()

    session = build_managed_session()
    session.risk_plans.clear()

    result = service.audit(session)

    assert result.valid is False
    assert any(
        "RiskPlan is missing" in error
        for error in result.errors
    )


def test_orphan_lifecycle_state_is_rejected():
    service = TradingSessionIntegrityService()

    session = build_managed_session()
    session.portfolio.positions.clear()

    result = service.audit(session)

    assert result.valid is False
    assert any(
        "orphan PositionState" in error
        for error in result.errors
    )
    assert any(
        "orphan RiskPlan" in error
        for error in result.errors
    )


def test_mismatched_current_price_is_rejected():
    service = TradingSessionIntegrityService()

    session = build_managed_session()
    session.position_states["AAPL"] = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=100.7,
        highest_price=106.0,
        current_price=105.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=False,
        target_3_hit=False,
    )

    result = service.audit(session)

    assert result.valid is False
    assert any(
        "current_price" in error
        for error in result.errors
    )


def test_repository_refuses_invalid_save():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()

    session = build_managed_session()
    session.risk_plans.clear()

    try:
        repository.save(session)
    except TradingSessionIntegrityError as error:
        assert "RiskPlan is missing" in str(error)
    else:
        raise AssertionError(
            "Expected TradingSessionIntegrityError."
        )

    assert repository.exists() is False


def test_repository_rejects_invalid_loaded_json():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()
    TEST_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    session = build_managed_session()
    session.risk_plans.clear()

    serializer = DataclassSerializer()

    TEST_PATH.write_text(
        json.dumps(
            serializer.to_dict(session),
            indent=2,
        ),
        encoding="utf-8",
    )

    try:
        repository.load()
    except TradingSessionIntegrityError as error:
        assert "RiskPlan is missing" in str(error)
    else:
        raise AssertionError(
            "Expected TradingSessionIntegrityError."
        )
    finally:
        repository.delete()


def main():
    print()
    print("=========================================")
    print("TRADING SESSION INTEGRITY TEST")
    print("=========================================")
    print()

    test_complete_managed_session_is_valid()
    test_legacy_position_without_lifecycle_is_allowed()
    test_half_managed_position_is_rejected()
    test_orphan_lifecycle_state_is_rejected()
    test_mismatched_current_price_is_rejected()
    test_repository_refuses_invalid_save()
    test_repository_rejects_invalid_loaded_json()

    print("TRADING SESSION INTEGRITY: PASS")


if __name__ == "__main__":
    main()
