from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper
from services.ibkr.ibkr_portfolio_service import IbkrPortfolioService
from services.paper_trading_pipeline_adapter import (
    PaperTradingPipelineAdapter,
)
from services.market.fx_rate_service import FxRate


@dataclass(frozen=True)
class FakeIndicatorPack:
    symbol: str


class FixedFxRateService:
    def get_rate(self, from_currency: str, to_currency: str) -> FxRate:
        return FxRate(
            from_currency=from_currency,
            to_currency=to_currency,
            rate=0.80 if from_currency != to_currency else 1.0,
            source="test",
        )


class FakeAccountService:
    def __init__(self) -> None:
        self.account_reads = 0
        self.position_reads = 0

    def read_account(self) -> BrokerAccount:
        self.account_reads += 1

        return BrokerAccount(
            broker_name="IBKR",
            account_id="DU123456",
            cash=9723.26,
            buying_power=66049.0,
            currency="EUR",
            status="ACTIVE",
        )

    def read_positions(self) -> list[BrokerPosition]:
        self.position_reads += 1

        return [
            BrokerPosition(
                account_id="DU123456",
                symbol="AAPL",
                security_type="STK",
                exchange="SMART",
                currency="USD",
                quantity=1.0,
                average_cost=316.58,
            )
        ]


class FakeIndicatorBuilder:
    def __init__(self) -> None:
        self.build_called = False
        self.received_symbol: str | None = None
        self.received_history: pd.DataFrame | None = None

    def build(
        self,
        *,
        symbol: str,
        history: pd.DataFrame,
    ) -> FakeIndicatorPack:
        self.build_called = True
        self.received_symbol = symbol
        self.received_history = history

        return FakeIndicatorPack(
            symbol=symbol,
        )


class FakeTradingPipeline:
    def __init__(self) -> None:
        self.run_called = False
        self.received_indicator_data = None
        self.received_portfolio_state = None

    def run(
        self,
        *,
        indicator_data,
        portfolio_state,
    ) -> TradingPipelineResult:
        self.run_called = True
        self.received_indicator_data = indicator_data
        self.received_portfolio_state = portfolio_state

        risk_plan = RiskPlan(
            symbol=indicator_data.symbol,
            entry_price=315.58,
            stop_loss=300.0,
            target_1=325.0,
            target_2=335.0,
            target_3=345.0,
            risk_percent=4.94,
            reward_percent=2.99,
            risk_reward_ratio=0.61,
            confidence=0.80,
            notes="Fake IBKR portfolio pipeline test",
        )

        return TradingPipelineResult(
            symbol=indicator_data.symbol,
            decision="HOLD",
            confidence=0.80,
            position_size=0.0,
            expected_risk=0.0,
            risk_plan=risk_plan,
            market_intelligence=None,
            ai_context=None,
            explanation="Fake pipeline result.",
            investment_thesis=None,
        )


def build_history() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Open": 314.0,
                "High": 317.0,
                "Low": 313.0,
                "Close": 315.58,
                "Volume": 1000000,
            }
        ]
    )


def test_ibkr_portfolio_is_passed_to_existing_pipeline() -> None:
    account_service = FakeAccountService()

    portfolio_service = IbkrPortfolioService(
        account_service=account_service,
        mapper=IbkrPortfolioMapper(
            fx_rate_service=FixedFxRateService(),
            require_live_fx=True,
        ),
    )

    portfolio = portfolio_service.read_portfolio(
        current_prices={
            "AAPL": 315.58,
        }
    )

    indicator_builder = FakeIndicatorBuilder()
    trading_pipeline = FakeTradingPipeline()

    adapter = PaperTradingPipelineAdapter(
        indicator_builder=indicator_builder,
        trading_pipeline=trading_pipeline,
    )

    history = build_history()

    result = adapter.run(
        symbol="aapl",
        history=history,
        portfolio_state=portfolio,
    )

    assert account_service.account_reads == 1
    assert account_service.position_reads == 1

    assert portfolio.cash == 9723.26
    assert portfolio.equity == 9975.72
    assert set(portfolio.positions) == {"AAPL"}

    position = portfolio.positions["AAPL"]

    assert position.quantity == 1
    assert position.entry_price == 316.58
    assert position.current_price == 315.58

    assert indicator_builder.build_called is True
    assert indicator_builder.received_symbol == "AAPL"
    assert indicator_builder.received_history is history

    assert trading_pipeline.run_called is True
    assert (
        trading_pipeline.received_portfolio_state
        is portfolio
    )
    assert (
        trading_pipeline.received_indicator_data.symbol
        == "AAPL"
    )

    assert result.symbol == "AAPL"
    assert result.decision == "HOLD"
    assert result.confidence == 0.80
    assert result.risk_plan.symbol == "AAPL"


def run() -> None:
    test_ibkr_portfolio_is_passed_to_existing_pipeline()

    print(
        "PASS: "
        "test_ibkr_portfolio_is_passed_to_existing_pipeline"
    )
    print()
    print("IBKR PORTFOLIO PIPELINE TESTS: 1 passed")


if __name__ == "__main__":
    run()
