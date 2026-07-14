from __future__ import annotations

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper
from services.ibkr.ibkr_portfolio_service import (
    IbkrPortfolioService,
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


def create_service() -> tuple[IbkrPortfolioService, FakeAccountService]:
    account_service = FakeAccountService()

    service = IbkrPortfolioService(
        account_service=account_service,
        mapper=IbkrPortfolioMapper(),
    )

    return service, account_service


def test_reads_account() -> None:
    service, fake = create_service()

    account = service.read_account()

    assert account.account_id == "DU123456"
    assert account.cash == 9723.26
    assert fake.account_reads == 1


def test_reads_positions() -> None:
    service, fake = create_service()

    positions = service.read_positions()

    assert len(positions) == 1
    assert positions[0].symbol == "AAPL"
    assert fake.position_reads == 1


def test_builds_complete_portfolio() -> None:
    service, fake = create_service()

    portfolio = service.read_portfolio(
        current_prices={
            "AAPL": 315.58,
        }
    )

    assert fake.account_reads == 1
    assert fake.position_reads == 1

    assert portfolio.cash == 9723.26
    assert portfolio.positions_value == 315.58
    assert portfolio.equity == 10038.84

    assert "AAPL" in portfolio.positions

    position = portfolio.positions["AAPL"]

    assert position.quantity == 1
    assert position.entry_price == 316.58
    assert position.current_price == 315.58


def run() -> None:
    tests = [
        test_reads_account,
        test_reads_positions,
        test_builds_complete_portfolio,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        f"IBKR PORTFOLIO SERVICE TESTS: {len(tests)} passed"
    )


if __name__ == "__main__":
    run()