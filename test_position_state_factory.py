from models.risk_plan import RiskPlan
from services.position_state_factory import PositionStateFactory


def run():

    factory = PositionStateFactory()

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

    print(state)

    assert state.symbol == "AAPL"
    assert state.entry_price == 100.0
    assert state.current_stop_loss == 95.0
    assert state.highest_price == 100.0
    assert state.current_price == 100.0

    assert state.break_even_active is False
    assert state.trailing_stop_active is False

    assert state.target_1_hit is False
    assert state.target_2_hit is False
    assert state.target_3_hit is False

    print("PASS")


if __name__ == "__main__":
    run()