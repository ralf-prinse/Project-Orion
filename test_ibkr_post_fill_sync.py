from __future__ import annotations

from dataclasses import dataclass

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


@dataclass
class DummyState:
    symbol: str


@dataclass
class DummyRiskPlan:
    symbol: str


class SequencedIbkrAccountService:
    """
    Returns a predetermined position snapshot on every read.

    This simulates delayed IBKR portfolio propagation after a fill.
    """

    def __init__(
        self,
        *,
        positions_sequence: list[
            tuple[BrokerPosition, ...]
        ],
        cash: float = 9450.0,
    ) -> None:
        if not positions_sequence:
            raise ValueError(
                "positions_sequence must not be empty."
            )

        self.positions_sequence = positions_sequence
        self.cash = cash

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
            cash=self.cash,
            buying_power=20000.0,
            currency="EUR",
            status="ACTIVE",
        )

    def read_positions(
        self,
    ) -> tuple[BrokerPosition, ...]:
        index = min(
            self.read_positions_calls,
            len(self.positions_sequence) - 1,
        )

        self.read_positions_calls += 1

        return self.positions_sequence[index]


class FakePriceProvider:
    def __init__(
        self,
        *,
        prices: dict[str, float],
    ) -> None:
        self.prices = {
            symbol.strip().upper(): float(price)
            for symbol, price in prices.items()
        }
        self.requested_symbols: list[str] = []

    def get_current_price(
        self,
        symbol: str,
    ) -> float:
        normalized_symbol = symbol.strip().upper()
        self.requested_symbols.append(normalized_symbol)

        return self.prices[normalized_symbol]


def create_session(
    *,
    cash: float,
    positions: dict[str, PaperPosition],
) -> TradingSession:
    return TradingSession(
        name="IBKR post-fill sync test",
        portfolio=PaperPortfolio(
            cash=cash,
            positions=positions,
        ),
        position_states={
            symbol: DummyState(symbol=symbol)
            for symbol in positions
        },
        risk_plans={
            symbol: DummyRiskPlan(symbol=symbol)
            for symbol in positions
        },
    )


def test_sync_waits_for_expected_filled_symbol() -> None:
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

    account_service = SequencedIbkrAccountService(
        positions_sequence=[
            existing_positions,
            existing_positions
            + (
                create_position(
                    symbol="F",
                    quantity=10.0,
                    average_cost=14.221,
                ),
            ),
        ],
    )

    price_provider = FakePriceProvider(
        prices={
            "AAPL": 320.0,
            "AAL": 16.0,
            "F": 14.25,
        },
    )

    sync_service = IbkrTradingSessionSyncService(
        account_service=account_service,
        price_provider=price_provider,
    )

    session = create_session(
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
    )

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


def test_post_fill_sync_removes_fully_sold_position() -> None:
    account_service = SequencedIbkrAccountService(
        positions_sequence=[
            (
                create_position(
                    symbol="AAPL",
                    quantity=2.0,
                    average_cost=100.0,
                ),
            ),
            (),
        ],
        cash=1020.0,
    )

    price_provider = FakePriceProvider(
        prices={
            "AAPL": 110.0,
        },
    )

    service = IbkrTradingSessionSyncService(
        account_service=account_service,
        price_provider=price_provider,
    )

    session = create_session(
        cash=800.0,
        positions={
            "AAPL": PaperPosition(
                symbol="AAPL",
                quantity=2,
                entry_price=100.0,
                current_price=110.0,
            ),
        },
    )

    synchronized = service.synchronize(
        session,
        expected_position_quantities={
            "AAPL": 0,
        },
        attempts=2,
        retry_delay_seconds=0.0,
    )

    assert account_service.connect_calls == 1
    assert account_service.disconnect_calls == 1
    assert account_service.read_positions_calls == 2

    assert synchronized.portfolio.cash == 1020.0
    assert "AAPL" not in synchronized.portfolio.positions
    assert "AAPL" not in synchronized.position_states
    assert "AAPL" not in synchronized.risk_plans

    # No price request is necessary for a fully closed position.
    assert price_provider.requested_symbols == []


def test_post_fill_sync_keeps_partially_sold_position() -> None:
    account_service = SequencedIbkrAccountService(
        positions_sequence=[
            (
                create_position(
                    symbol="AAPL",
                    quantity=5.0,
                    average_cost=100.0,
                ),
            ),
            (
                create_position(
                    symbol="AAPL",
                    quantity=3.0,
                    average_cost=100.0,
                ),
            ),
        ],
        cash=720.0,
    )

    price_provider = FakePriceProvider(
        prices={
            "AAPL": 110.0,
        },
    )

    service = IbkrTradingSessionSyncService(
        account_service=account_service,
        price_provider=price_provider,
    )

    session = create_session(
        cash=500.0,
        positions={
            "AAPL": PaperPosition(
                symbol="AAPL",
                quantity=5,
                entry_price=100.0,
                current_price=110.0,
            ),
        },
    )

    synchronized = service.synchronize(
        session,
        expected_position_quantities={
            "AAPL": 3,
        },
        attempts=2,
        retry_delay_seconds=0.0,
    )

    assert account_service.connect_calls == 1
    assert account_service.disconnect_calls == 1
    assert account_service.read_positions_calls == 2

    assert synchronized.portfolio.cash == 720.0
    assert "AAPL" in synchronized.portfolio.positions

    position = synchronized.portfolio.positions["AAPL"]

    assert position.quantity == 3
    assert position.entry_price == 100.0
    assert position.current_price == 110.0

    assert "AAPL" in synchronized.position_states
    assert "AAPL" in synchronized.risk_plans

    assert price_provider.requested_symbols == ["AAPL"]


def run() -> None:
    tests = [
        test_sync_waits_for_expected_filled_symbol,
        test_post_fill_sync_removes_fully_sold_position,
        test_post_fill_sync_keeps_partially_sold_position,
    ]

    passed = 0

    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR POST-FILL SYNC TESTS: "
        f"{passed} passed"
    )


if __name__ == "__main__":
    run()