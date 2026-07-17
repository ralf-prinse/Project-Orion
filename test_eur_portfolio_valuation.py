from __future__ import annotations

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.ibkr.ibkr_portfolio_mapper import (
    IbkrPortfolioMapper,
    IbkrPortfolioMappingError,
)
from services.market.fx_rate_service import FxRate
from services.portfolio_allocator import PortfolioAllocator
from test_portfolio_allocator import _candidate


class FixedFxRateService:
    def __init__(self, rate: float = 0.80, source: str = "test") -> None:
        self.rate = rate
        self.source = source

    def get_rate(self, from_currency: str, to_currency: str) -> FxRate:
        rate = 1.0 if from_currency == to_currency else self.rate
        source = "identity" if from_currency == to_currency else self.source
        return FxRate(from_currency, to_currency, rate, source)


def eur_account(currency: str = "EUR") -> BrokerAccount:
    return BrokerAccount(
        broker_name="IBKR",
        account_id="DU123456",
        cash=1000.0,
        buying_power=5000.0,
        currency=currency,
        status="ACTIVE",
    )


def usd_position() -> BrokerPosition:
    return BrokerPosition(
        account_id="DU123456",
        symbol="AAPL",
        security_type="STK",
        exchange="NASDAQ",
        currency="USD",
        quantity=2.0,
        average_cost=100.0,
    )


def test_ibkr_portfolio_values_us_position_in_euro() -> None:
    mapper = IbkrPortfolioMapper(
        fx_rate_service=FixedFxRateService(),
        require_live_fx=True,
    )

    portfolio = mapper.map(
        account=eur_account(),
        positions=(usd_position(),),
        current_prices={"AAPL": 110.0},
    )

    assert portfolio.base_currency == "EUR"
    assert portfolio.positions["AAPL"].currency == "USD"
    assert portfolio.positions["AAPL"].market_value == 176.0
    assert portfolio.positions_value == 176.0
    assert portfolio.equity == 1176.0


def test_ibkr_mapper_rejects_non_euro_base_account() -> None:
    mapper = IbkrPortfolioMapper(
        fx_rate_service=FixedFxRateService(),
    )

    try:
        mapper.map(
            account=eur_account(currency="USD"),
            positions=(),
            current_prices={},
        )
    except IbkrPortfolioMappingError as exc:
        assert "base currency must be EUR" in str(exc)
    else:
        raise AssertionError("Expected non-EUR account to fail closed.")


def test_strict_mapper_rejects_fallback_fx() -> None:
    mapper = IbkrPortfolioMapper(
        fx_rate_service=FixedFxRateService(source="fallback"),
        require_live_fx=True,
    )

    try:
        mapper.map(
            account=eur_account(),
            positions=(usd_position(),),
            current_prices={"AAPL": 110.0},
        )
    except IbkrPortfolioMappingError as exc:
        assert "Validated FX rate unavailable" in str(exc)
    else:
        raise AssertionError("Expected fallback FX to fail closed.")


def test_allocator_sizes_us_candidate_in_euro() -> None:
    allocator = PortfolioAllocator(
        fx_rate_service=FixedFxRateService(),
        require_live_fx=True,
    )
    session = TradingSession(
        name="EUR allocation",
        portfolio=PaperPortfolio(cash=1000.0, base_currency="EUR"),
        peak_portfolio_value=1000.0,
    )
    config = LivePaperTradingConfig(
        max_position_value=160.0,
        max_position_size_pct=1.0,
        max_portfolio_exposure=1.0,
        min_cash_reserve_pct=0.0,
        max_risk_per_trade_pct=1.0,
        max_portfolio_risk_pct=1.0,
    )

    result = allocator.allocate(
        session=session,
        candidates=[_candidate("AAPL", 100.0, 0.9, 90.0)],
        config=config,
    )

    assert result.approved_count == 1
    assert result.approved[0].quantity == 2
    assert result.approved[0].estimated_value == 160.0


def test_allocator_rejects_fallback_fx() -> None:
    allocator = PortfolioAllocator(
        fx_rate_service=FixedFxRateService(source="fallback"),
        require_live_fx=True,
    )
    session = TradingSession(
        name="EUR allocation",
        portfolio=PaperPortfolio(cash=1000.0, base_currency="EUR"),
    )

    result = allocator.allocate(
        session=session,
        candidates=[_candidate("AAPL", 100.0, 0.9, 90.0)],
        config=LivePaperTradingConfig(),
    )

    assert result.approved_count == 0
    assert "validated FX rate unavailable" in result.rejected[0].reason
