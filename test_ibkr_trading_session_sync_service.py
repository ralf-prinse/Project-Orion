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


class FakeIbkrAccountService:
    def __init__(self) -> None:
        self.connect_called = False
        self.disconnect_called = False

    def connect(self) -> None:
        self.connect_called = True

    def disconnect(self) -> None:
        self.disconnect_called = True

    def read_account(self) -> BrokerAccount:
        return BrokerAccount(
            broker_name="IBKR",
            account_id="DU123456",
            cash=8500.0,
            buying_power=20000.0,
            currency="EUR",
            status="ACTIVE",
        )

    def read_positions(self) -> list[BrokerPosition]:
        return [
            BrokerPosition(
                account_id="DU123456",
                symbol="AAPL",
                quantity=1.0,
                average_cost=315.58,
                currency="USD",
                security_type="STK",
                exchange="NASDAQ",
            ),
            BrokerPosition(
                account_id="DU123456",
                symbol="AAL",
                quantity=9.0,
                average_cost=15.7711,
                currency="USD",
                security_type="STK",
                exchange="NASDAQ",
            ),
        ]


class FakePriceProvider:
    def __init__(self) -> None:
        self.requested_symbols: list[str] = []

    def get_current_price(self, symbol: str) -> float:
        self.requested_symbols.append(symbol)

        prices = {
            "AAPL": 320.0,
            "AAL": 16.0,
        }

        return prices[symbol]


@dataclass
class DummyState:
    symbol: str


@dataclass
class DummyRiskPlan:
    symbol: str


def create_session() -> TradingSession:
    return TradingSession(
        name="IBKR sync test",
        portfolio=PaperPortfolio(
            cash=1000.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=1,
                    entry_price=300.0,
                    current_price=305.0,
                ),
                "MSFT": PaperPosition(
                    symbol="MSFT",
                    quantity=2,
                    entry_price=200.0,
                    current_price=210.0,
                ),
            },
        ),
        position_states={
            "AAPL": DummyState(symbol="AAPL"),
            "MSFT": DummyState(symbol="MSFT"),
        },
        risk_plans={
            "AAPL": DummyRiskPlan(symbol="AAPL"),
            "MSFT": DummyRiskPlan(symbol="MSFT"),
        },
    )


def test_sync_replaces_portfolio_with_ibkr_truth() -> None:
    account_service = FakeIbkrAccountService()
    price_provider = FakePriceProvider()

    service = IbkrTradingSessionSyncService(
        account_service=account_service,
        price_provider=price_provider,
    )

    session = create_session()

    result = service.synchronize(session)

    assert result is session
    assert account_service.connect_called is True
    assert account_service.disconnect_called is True

    assert result.cash == 8500.0
    assert result.open_positions == 2
    assert set(result.portfolio.positions) == {"AAPL", "AAL"}

    assert result.portfolio.positions["AAPL"].quantity == 1
    assert result.portfolio.positions["AAPL"].entry_price == 315.58
    assert result.portfolio.positions["AAPL"].current_price == 320.0

    assert result.portfolio.positions["AAL"].quantity == 9
    assert result.portfolio.positions["AAL"].entry_price == 15.7711
    assert result.portfolio.positions["AAL"].current_price == 16.0

    assert price_provider.requested_symbols == ["AAPL", "AAL"]


def test_sync_removes_stale_local_lifecycle_state() -> None:
    service = IbkrTradingSessionSyncService(
        account_service=FakeIbkrAccountService(),
        price_provider=FakePriceProvider(),
    )

    session = create_session()

    result = service.synchronize(session)

    assert set(result.position_states) == {"AAPL"}
    assert set(result.risk_plans) == {"AAPL"}

    assert "MSFT" not in result.position_states
    assert "MSFT" not in result.risk_plans


def test_sync_restores_known_euronext_symbol_suffix() -> None:
    service = IbkrTradingSessionSyncService(
        account_service=FakeIbkrAccountService(),
        price_provider=FakePriceProvider(),
    )
    session = TradingSession(
        name="Known Euronext position",
        portfolio=PaperPortfolio(
            cash=9000.0,
            positions={
                "ASML.AS": PaperPosition(
                    symbol="ASML.AS",
                    quantity=1,
                    entry_price=1200.0,
                    current_price=1210.0,
                ),
            },
        ),
        position_states={"ASML.AS": DummyState(symbol="ASML.AS")},
        risk_plans={"ASML.AS": DummyRiskPlan(symbol="ASML.AS")},
    )
    broker_position = BrokerPosition(
        account_id="DU123456",
        symbol="ASML",
        quantity=1.0,
        average_cost=1200.0,
        currency="EUR",
        security_type="STK",
        exchange="AEB",
    )

    restored = service._restore_orion_symbols(
        broker_positions=(broker_position,),
        session=session,
    )

    assert restored[0].symbol == "ASML.AS"


def test_sync_maps_unknown_aeb_position_to_euronext_symbol() -> None:
    service = IbkrTradingSessionSyncService(
        account_service=FakeIbkrAccountService(),
        price_provider=FakePriceProvider(),
    )
    broker_position = BrokerPosition(
        account_id="DU123456",
        symbol="ASM",
        quantity=1.0,
        average_cost=870.0,
        currency="EUR",
        security_type="STK",
        exchange="AEB",
    )

    restored = service._restore_orion_symbols(
        broker_positions=(broker_position,),
        session=TradingSession(
            name="Empty session",
            portfolio=PaperPortfolio(cash=1000.0),
        ),
    )

    assert restored[0].symbol == "ASM.AS"


def run() -> None:
    tests = [
        test_sync_replaces_portfolio_with_ibkr_truth,
        test_sync_removes_stale_local_lifecycle_state,
        test_sync_restores_known_euronext_symbol_suffix,
        test_sync_maps_unknown_aeb_position_to_euronext_symbol,
    ]

    passed = 0

    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR TRADING SESSION SYNC TESTS: "
        f"{passed} passed"
    )


if __name__ == "__main__":
    run()
