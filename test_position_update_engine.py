from models.risk_plan import RiskPlan
from services.position_state_factory import PositionStateFactory
from services.position_update_engine import PositionUpdateEngine
from datetime import UTC, datetime

def run():

    factory = PositionStateFactory()
    engine = PositionUpdateEngine()

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

    state = factory.create(plan)

    opened_at = datetime(
        2026,
        7,
        10,
        9,
        0,
        tzinfo=UTC,
    )

    state.opened_at = opened_at

    print("========== UPDATE ==========")

    result = engine.update(
        state=state,
        risk_plan=plan,
        current_price=112.0,
    )

    print(result)

    assert result.state.break_even_active is True
    assert result.state.current_stop_loss > plan.entry_price
    assert result.state.highest_price == 112.0
    assert result.state.target_1_hit is True
    assert result.state.target_2_hit is False
    assert result.state.target_3_hit is False
    assert result.state.opened_at == opened_at

    print("PASS")


if __name__ == "__main__":
    run()