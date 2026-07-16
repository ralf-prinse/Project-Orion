from __future__ import annotations

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.trading_session import TradingSession
from services.ibkr.ibkr_trading_session_sync_service import (
    IbkrTradingSessionSyncService,
)


def create_position(
    symbol: str,
    quantity: float,
    average_cost: float,
) -> BrokerPosition:
    return BrokerPosition(
        account_id="DU123456",
        symbol=symbol,
        security_type="STK",
        exchange="NASDAQ",
        currency="USD",
        quantity=quantity,
        average_cost=average_cost,
    )


class DelayedPositionAccountService:
    """
    Simulates IBKR position propagation after a fill.

    First read:
        AAPL and AAL only.

    Second read:
        AAPL, AAL and newly filled F position.
    """

    def __init__(self) -> None:
        self.connect_calls = 0
        self.disconnect_calls = 0
        self.read_positions_calls = 0

    def connect(self) -> None:
        self.connect_calls += 1

    def disconnect(self) -> None:
        self.disconnect_calls += 1

    def read_account(self) -> BrokerAccount:
        return BrokerAccount(
            broker_name="IBKR",
            account_id="DU123456",
            cash=9450.0,
            buying_power=20000.0,
            currency="EUR",
            status="ACTIVE",
        )

    def read_positions(
        self,
    ) -> tuple[BrokerPosition, ...]:
        self.read_positions_calls += 1

        existing_positions = (
            create_position(
                symbol="AAPL",
                quantity=1.0,
                average_cost=315.58,
            ),
            create_position(
                symbol="AAL",
                quantity=9.0,
                average_cost=15.7711,
            ),
        )

        if self.read_positions_calls == 1:
            return existing_positions

        return existing_positions + (
            create_position(
                symbol="F",
                quantity=10.0,
                average_cost=14.221,
            ),
        )


class FakePriceProvider:
    def get_current_price(
        self,
        symbol: str,
    ) -> float:
        prices = {
            "AAPL": 320.0,
            "AAL": 16.0,
            "F": 14.25,
        }

        return prices[symbol]


def create_session() -> TradingSession:
    return TradingSession(
        name="IBKR post-fill sync test",
        portfolio=PaperPortfolio(
            cash=9600.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=1,
                    entry_price=315.58,
                    current_price=320.0,
                ),
                "AAL": PaperPosition(
                    symbol="AAL",
                    quantity=9,
                    entry_price=15.7711,
                    current_price=16.0,
                ),
            },
        ),
    )


def test_sync_waits_for_expected_filled_symbol() -> None:
    account_service = DelayedPositionAccountService()

    sync_service = IbkrTradingSessionSyncService(
        account_service=account_service,
        price_provider=FakePriceProvider(),
    )

    session = create_session()

    result = sync_service.synchronize(
        session,
        expected_symbols={"F"},
        attempts=4,
        retry_delay_seconds=0.0,
    )

    assert result is session
    assert account_service.connect_calls == 1
    assert account_service.disconnect_calls == 1
    assert account_service.read_positions_calls == 2

    assert set(result.portfolio.positions) == {
        "AAPL",
        "AAL",
        "F",
    }

    assert result.portfolio.positions["F"].quantity == 10
    assert result.portfolio.positions["F"].entry_price == 14.221
    assert result.portfolio.positions["F"].current_price == 14.25


def run() -> None:
    test_sync_waits_for_expected_filled_symbol()

    print(
        "PASS: test_sync_waits_for_expected_filled_symbol"
    )
    print()
    print("IBKR POST-FILL SYNC TESTS: 1 passed")


if __name__ == "__main__":
    run()