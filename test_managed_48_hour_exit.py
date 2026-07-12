from datetime import UTC, datetime, timedelta

from models.live_paper_trading_config import (
    LivePaperTradingConfig,
)
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.position_monitor import PositionMonitor


def build_position() -> PaperPosition:
    return PaperPosition(
        symbol="AAPL",
        quantity=2,
        entry_price=100.0,
        current_price=102.0,
    )


def build_state(
    opened_at: datetime,
) -> PositionState:
    return PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=103.0,
        current_price=102.0,
        opened_at=opened_at,
    )


def build_risk_plan() -> RiskPlan:
    return RiskPlan(
        symbol="AAPL",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=104.0,
        target_2=106.0,
        target_3=108.0,
        risk_percent=5.0,
        reward_percent=8.0,
        risk_reward_ratio=1.6,
        confidence=0.85,
        notes="Managed 48-hour exit test.",
    )


def test_managed_position_holds_before_48_hours():
    opened_at = datetime(
        2026,
        7,
        10,
        9,
        0,
        tzinfo=UTC,
    )

    result = PositionMonitor().evaluate_managed(
        position=build_position(),
        state=build_state(opened_at),
        risk_plan=build_risk_plan(),
        config=LivePaperTradingConfig(
            max_holding_days=2,
        ),
        now=opened_at + timedelta(
            hours=47,
            minutes=59,
        ),
    )

    assert result.action == "HOLD"


def test_managed_position_exits_at_48_hours():
    opened_at = datetime(
        2026,
        7,
        10,
        9,
        0,
        tzinfo=UTC,
    )

    result = PositionMonitor().evaluate_managed(
        position=build_position(),
        state=build_state(opened_at),
        risk_plan=build_risk_plan(),
        config=LivePaperTradingConfig(
            max_holding_days=2,
        ),
        now=opened_at + timedelta(hours=48),
    )

    assert result.action == "MAX_HOLDING_TIME"
    assert (
        result.reason
        == "Maximum holding period reached."
    )


def run():
    test_managed_position_holds_before_48_hours()
    test_managed_position_exits_at_48_hours()

    print("MANAGED 48-HOUR EXIT: PASS")


if __name__ == "__main__":
    run()