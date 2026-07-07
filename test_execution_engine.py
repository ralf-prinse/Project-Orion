from models.execution_context import ExecutionContext
from models.execution_request import ExecutionRequest
from models.paper_portfolio import PaperPortfolio
from models.risk_plan import RiskPlan
from services.execution_engine import ExecutionEngine


def run():
    engine = ExecutionEngine()

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

    request = ExecutionRequest(
        symbol="AAPL",
        action="OPEN_POSITION",
        entry_price=100.0,
        quantity=2,
        risk_plan=plan,
        confidence=0.90,
    )

    context = ExecutionContext(
        request=request,
        portfolio=PaperPortfolio(cash=1000.0),
        max_position_percentage=0.50,
    )

    result = engine.execute(context)

    print(result)

    assert result.validation.is_valid is True
    assert result.execution.accepted is True
    assert result.execution.status == "FILLED"
    assert result.portfolio.cash == 800.0
    assert "AAPL" in result.portfolio.positions
    assert result.snapshot.equity == 1000.0
    assert result.report.status == "FILLED"

    print("PASS")


if __name__ == "__main__":
    run()