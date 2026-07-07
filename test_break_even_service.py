from services.risk.break_even_service import BreakEvenService
from models.risk_plan import RiskPlan


def run():

    service = BreakEvenService()

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

    result = service.evaluate(
        risk_plan=plan,
        current_price=108.0,
    )

    print(result)

    assert result.activated is False
    assert result.new_stop_loss == 95.0

    print("PASS")

    print()

    print("========== AFTER TARGET ==========")

    result = service.evaluate(
        risk_plan=plan,
        current_price=112.0,
    )

    print(result)

    assert result.activated is True
    assert result.new_stop_loss == 100.0

    print("PASS")


if __name__ == "__main__":
    run()