from __future__ import annotations

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from services.ibkr.ibkr_portfolio_mapper import (
    IbkrPortfolioMapper,
    IbkrPortfolioMappingError,
)


def create_account(
    *,
    broker_name: str = "IBKR",
    account_id: str = "DU123456",
    cash: float = 10000.0,
    buying_power: float = 50000.0,
    currency: str = "EUR",
    status: str = "ACTIVE",
) -> BrokerAccount:
    return BrokerAccount(
        broker_name=broker_name,
        account_id=account_id,
        cash=cash,
        buying_power=buying_power,
        currency=currency,
        status=status,
    )


def create_position(
    *,
    account_id: str = "DU123456",
    symbol: str = "AAPL",
    security_type: str = "STK",
    exchange: str = "SMART",
    currency: str = "USD",
    quantity: float = 2.0,
    average_cost: float = 100.0,
) -> BrokerPosition:
    return BrokerPosition(
        account_id=account_id,
        symbol=symbol,
        security_type=security_type,
        exchange=exchange,
        currency=currency,
        quantity=quantity,
        average_cost=average_cost,
    )


def test_maps_empty_broker_portfolio() -> None:
    mapper = IbkrPortfolioMapper()

    portfolio = mapper.map(
        account=create_account(),
        positions=(),
        current_prices={},
    )

    assert portfolio.cash == 10000.0
    assert portfolio.positions == {}
    assert portfolio.positions_value == 0
    assert portfolio.equity == 10000.0


def test_maps_single_broker_position() -> None:
    mapper = IbkrPortfolioMapper()

    portfolio = mapper.map(
        account=create_account(
            cash=9723.26,
        ),
        positions=[
            create_position(
                symbol=" aapl ",
                quantity=1.0,
                average_cost=316.58,
            )
        ],
        current_prices={
            "AAPL": 315.58,
        },
    )

    assert portfolio.cash == 9723.26
    assert set(portfolio.positions) == {"AAPL"}

    position = portfolio.positions["AAPL"]

    assert position.symbol == "AAPL"
    assert position.quantity == 1
    assert position.entry_price == 316.58
    assert position.current_price == 315.58
    assert position.cost_basis == 316.58
    assert position.market_value == 315.58
    assert position.unrealized_profit_loss == -1.0

    assert portfolio.positions_value == 315.58
    assert portfolio.equity == 10038.84


def test_maps_multiple_positions() -> None:
    mapper = IbkrPortfolioMapper()

    portfolio = mapper.map(
        account=create_account(
            cash=5000.0,
        ),
        positions=[
            create_position(
                symbol="AAPL",
                quantity=2.0,
                average_cost=100.0,
            ),
            create_position(
                symbol="MSFT",
                quantity=3.0,
                average_cost=200.0,
            ),
        ],
        current_prices={
            "aapl": 110.0,
            "msft": 210.0,
        },
    )

    assert portfolio.positions["AAPL"].quantity == 2
    assert portfolio.positions["MSFT"].quantity == 3
    assert portfolio.positions_value == 850.0
    assert portfolio.equity == 5850.0


def test_normalizes_account_and_symbol_case() -> None:
    mapper = IbkrPortfolioMapper()

    portfolio = mapper.map(
        account=create_account(
            broker_name=" ibkr ",
            account_id=" du123456 ",
            status=" active ",
        ),
        positions=[
            create_position(
                account_id="du123456",
                symbol=" msft ",
            )
        ],
        current_prices={
            "MSFT": 210.0,
        },
    )

    assert "MSFT" in portfolio.positions


def test_rejects_non_ibkr_account() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(
                broker_name="OTHER",
            ),
            positions=(),
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "only IBKR accounts" in str(exc)
    else:
        raise AssertionError(
            "Expected non-IBKR account to fail."
        )


def test_rejects_live_account() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(
                account_id="U123456",
            ),
            positions=(),
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "starting with 'DU'" in str(exc)
    else:
        raise AssertionError(
            "Expected live account to fail."
        )


def test_rejects_inactive_account() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(
                status="INACTIVE",
            ),
            positions=(),
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "must be ACTIVE" in str(exc)
    else:
        raise AssertionError(
            "Expected inactive account to fail."
        )


def test_rejects_negative_cash() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(
                cash=-1.0,
            ),
            positions=(),
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "cash must not be negative" in str(exc)
    else:
        raise AssertionError(
            "Expected negative cash to fail."
        )


def test_rejects_non_finite_buying_power() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(
                buying_power=float("nan"),
            ),
            positions=(),
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "buying power must be finite" in str(exc)
    else:
        raise AssertionError(
            "Expected non-finite buying power to fail."
        )


def test_rejects_position_for_other_account() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    account_id="DU999999",
                )
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "unexpected account" in str(exc)
    else:
        raise AssertionError(
            "Expected unexpected account to fail."
        )


def test_rejects_non_stock_position() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    security_type="OPT",
                )
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "only STK positions" in str(exc)
    else:
        raise AssertionError(
            "Expected non-stock position to fail."
        )


def test_rejects_zero_quantity() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    quantity=0.0,
                )
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero quantity to fail."
        )


def test_rejects_negative_quantity() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    quantity=-1.0,
                )
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected negative quantity to fail."
        )


def test_rejects_fractional_quantity() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    quantity=1.5,
                )
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "whole number" in str(exc)
    else:
        raise AssertionError(
            "Expected fractional quantity to fail."
        )


def test_rejects_missing_current_price() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(),
            ],
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "No validated current price" in str(exc)
    else:
        raise AssertionError(
            "Expected missing current price to fail."
        )


def test_rejects_zero_current_price() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(),
            ],
            current_prices={
                "AAPL": 0.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero current price to fail."
        )


def test_rejects_non_finite_current_price() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(),
            ],
            current_prices={
                "AAPL": float("inf"),
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "must be finite" in str(exc)
    else:
        raise AssertionError(
            "Expected non-finite current price to fail."
        )


def test_rejects_zero_average_cost() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    average_cost=0.0,
                )
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "Average cost" in str(exc)
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError(
            "Expected zero average cost to fail."
        )


def test_rejects_duplicate_positions() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=[
                create_position(
                    symbol="AAPL",
                ),
                create_position(
                    symbol="aapl",
                ),
            ],
            current_prices={
                "AAPL": 100.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "duplicate broker positions" in str(exc)
    else:
        raise AssertionError(
            "Expected duplicate positions to fail."
        )


def test_rejects_duplicate_normalized_price_symbols() -> None:
    mapper = IbkrPortfolioMapper()

    try:
        mapper.map(
            account=create_account(),
            positions=(),
            current_prices={
                "AAPL": 100.0,
                " aapl ": 101.0,
            },
        )
    except IbkrPortfolioMappingError as exc:
        assert "Duplicate current price" in str(exc)
    else:
        raise AssertionError(
            "Expected duplicate price symbols to fail."
        )


def run() -> None:
    tests = [
        test_maps_empty_broker_portfolio,
        test_maps_single_broker_position,
        test_maps_multiple_positions,
        test_normalizes_account_and_symbol_case,
        test_rejects_non_ibkr_account,
        test_rejects_live_account,
        test_rejects_inactive_account,
        test_rejects_negative_cash,
        test_rejects_non_finite_buying_power,
        test_rejects_position_for_other_account,
        test_rejects_non_stock_position,
        test_rejects_zero_quantity,
        test_rejects_negative_quantity,
        test_rejects_fractional_quantity,
        test_rejects_missing_current_price,
        test_rejects_zero_current_price,
        test_rejects_non_finite_current_price,
        test_rejects_zero_average_cost,
        test_rejects_duplicate_positions,
        test_rejects_duplicate_normalized_price_symbols,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR PORTFOLIO MAPPER TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()