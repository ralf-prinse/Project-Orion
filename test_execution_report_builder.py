from datetime import datetime

from models.execution_context import ExecutionContext
from models.execution_request import ExecutionRequest
from models.execution_result import ExecutionResult
from models.order import Order
from models.paper_portfolio import PaperPortfolio
from models.portfolio_snapshot import PortfolioSnapshot
from models.risk_plan import RiskPlan
from services.execution_report_builder import ExecutionReportBuilder


def run():
    builder = ExecutionReportBuilder()

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
    )

    order = Order(
        symbol="AAPL",
        side="BUY",
        quantity=2,
        order_type="MARKET",
        price=100.0,
        created_at=datetime.now(),
    )

    result = ExecutionResult(
        accepted=True,
        status="FILLED",
        order=order,
        message="Paper order filled.",
        executed_price=100.0,
        executed_quantity=2,
        executed_at=datetime.now(),
    )

    snapshot = PortfolioSnapshot(
        cash=800.0,
        equity=1000.0,
        positions_value=200.0,
        open_positions=1,
        realized_profit_loss=0.0,
        unrealized_profit_loss=0.0,
        created_at=datetime.now(),
    )

    report = builder.build(
        context=context,
        result=result,
        snapshot=snapshot,
    )

    print(report)

    assert report.symbol == "AAPL"
    assert report.status == "FILLED"
    assert report.cash == 800.0
    assert report.equity == 1000.0
    assert report.open_positions == 1

    print("PASS")


if __name__ == "__main__":
    run()