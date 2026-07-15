from __future__ import annotations

from datetime import datetime

from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_broker import IbkrBroker, IbkrOrderOutcome
from services.paper_trading_service import PaperTradingService
from services.trading_cycle import TradingCycle


class FakeIbkrTransport:
    def __init__(self) -> None:
        self.calls = 0
        self.contract = None
        self.order = None
        self.timeout_seconds = None

    def submit_order(self, *, contract, order, timeout_seconds):
        self.calls += 1
        self.contract = contract
        self.order = order
        self.timeout_seconds = timeout_seconds
        return IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=int(order.totalQuantity),
            average_fill_price=100.25,
            filled_at=datetime(2026, 7, 15, 19, 30, 0),
            message="Filled by fake IBKR transport.",
        )


def build_pipeline_result() -> TradingPipelineResult:
    risk_plan = RiskPlan(
        symbol="MSFT",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        target_3=130.0,
        risk_percent=5.0,
        reward_percent=10.0,
        risk_reward_ratio=2.0,
        confidence=0.90,
        notes="TradingCycle IBKR integration test",
    )
    return TradingPipelineResult(
        symbol="MSFT",
        decision="BUY",
        confidence=0.90,
        position_size=1.0,
        expected_risk=5.0,
        risk_plan=risk_plan,
        market_intelligence=None,
        ai_context=None,
        explanation="Test result",
        investment_thesis=None,
    )


def test_trading_cycle_opens_position_through_ibkr_broker() -> None:
    transport = FakeIbkrTransport()
    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=12.5,
        exchange="SMART",
        currency="USD",
    )
    execution_engine = ExecutionEngine(broker=broker)
    trading_service = PaperTradingService(execution_engine=execution_engine)
    cycle = TradingCycle(paper_trading_service=trading_service)

    session = TradingSession(
        name="IBKR integration test",
        portfolio=PaperPortfolio(cash=1000.0),
    )
    result = cycle.run(
        session=session,
        snapshot=MarketSnapshot(
            symbol="MSFT",
            current_price=100.0,
            pipeline_result=build_pipeline_result(),
        ),
        quantity=2,
    )

    assert transport.calls == 1
    assert transport.timeout_seconds == 12.5
    assert transport.contract.symbol == "MSFT"
    assert transport.contract.secType == "STK"
    assert transport.contract.exchange == "SMART"
    assert transport.contract.currency == "USD"
    assert transport.order.action == "BUY"
    assert transport.order.orderType == "MKT"
    assert transport.order.totalQuantity == 2
    assert transport.order.eTradeOnly is False
    assert transport.order.firmQuoteOnly is False
    assert transport.order.transmit is True

    assert result.action == "OPEN_POSITION"
    assert result.opened is not None
    assert result.opened.executed is True
    assert result.session.portfolio.cash == 799.50
    assert "MSFT" in result.session.portfolio.positions
    assert "MSFT" in result.session.position_states
    assert "MSFT" in result.session.risk_plans

    position = result.session.portfolio.positions["MSFT"]
    assert position.quantity == 2
    assert position.entry_price == 100.25
    assert position.current_price == 100.25


def run() -> None:
    test_trading_cycle_opens_position_through_ibkr_broker()
    print("PASS: test_trading_cycle_opens_position_through_ibkr_broker")
    print()
    print("TRADING CYCLE IBKR TESTS: 1 passed")


if __name__ == "__main__":
    run()
