from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.risk.position_health_service import PositionHealthService


def run():

    service = PositionHealthService()

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

    healthy_state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=106.0,
        highest_price=112.0,
        current_price=112.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=False,
        target_3_hit=False,
    )

    result = service.evaluate(
        state=healthy_state,
        risk_plan=plan,
    )

    print(result)

    assert result.status in {"EXCELLENT", "GOOD"}
    assert result.score >= 70

    weak_state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=100.0,
        current_price=96.0,
        break_even_active=False,
        trailing_stop_active=False,
        target_1_hit=False,
        target_2_hit=False,
        target_3_hit=False,
    )

    result = service.evaluate(
        state=weak_state,
        risk_plan=plan,
    )

    print(result)

    assert result.status in {"WEAK", "CRITICAL"}
    assert result.score < 70

    print("PASS")


if __name__ == "__main__":
    run()