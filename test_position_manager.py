from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.position_manager import PositionManager


def run():

    manager = PositionManager()

    plan = RiskPlan(
        symbol="AAPL",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        target_3=130.0,
        risk_percent=5.0,
        reward_percent=10.0,
        risk_reward_ratio=2.0,
        confidence=0.90,
        notes="test",
    )

    state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=110.0,
        current_price=110.0,
        break_even_active=False,
        trailing_stop_active=False,
        target_1_hit=False,
        target_2_hit=False,
        target_3_hit=False,
    )

    print("========== POSITION MANAGER ==========")

    result = manager.manage(
        state=state,
        risk_plan=plan,
        current_price=115.0,
    )

    print(result)

    assert result.stop_loss >= 100.0
    assert result.break_even is not None
    assert result.trailing_stop is not None
    assert len(result.actions) > 0

    print("PASS")


if __name__ == "__main__":
    run()