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

    print("========== BEFORE TARGET ==========")

    result = manager.manage(
        symbol="AAPL",
        risk_plan=plan,
        current_price=108.0,
    )

    print(result)

    assert result.stop_loss == 95.0
    assert "MOVE_STOP_TO_BREAK_EVEN" not in result.actions

    print("PASS")

    print()

    print("========== AFTER TARGET ==========")

    result = manager.manage(
        symbol="AAPL",
        risk_plan=plan,
        current_price=112.0,
    )

    print(result)

    assert result.stop_loss == 100.0
    assert "MOVE_STOP_TO_BREAK_EVEN" in result.actions

    print("PASS")


if __name__ == "__main__":
    run()