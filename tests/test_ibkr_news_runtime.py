from __future__ import annotations

from models.autonomous_paper_trading_config import AutonomousPaperTradingConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from services.ibkr.ibkr_autonomous_runtime_factory import IbkrAutonomousRuntimeFactory
from services.ibkr.ibkr_stock_contract_factory import IbkrStockContractFactory
from services.ibkr.ibkr_news_provider import IbkrNewsProvider


class FakeNewsProvider:
    name = "FAKE"

    def fetch_recent(self, **kwargs):
        return ()


def test_news_is_disabled_by_default():
    runtime = IbkrAutonomousRuntimeFactory().build(paper_account_id="DU123")

    assert runtime.news_provider is None
    assert runtime.news_intelligence_service is None


def test_shadow_news_provider_is_wired_without_connecting():
    provider = FakeNewsProvider()
    config = AutonomousPaperTradingConfig(
        live_config=LivePaperTradingConfig(news_mode="SHADOW")
    )

    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id="DU123",
        config=config,
        news_provider=provider,
    )

    assert runtime.news_provider is provider
    assert runtime.runner.news_intelligence_service is not None
    assert runtime.runner.news_intelligence_service.provider is provider


def test_contract_factory_maps_us_and_european_symbols():
    factory = IbkrStockContractFactory()

    us = factory.build("AAPL")
    amsterdam = factory.build("ASML.AS")
    germany = factory.build("SAP.DE")

    assert (us.symbol, us.exchange, us.currency) == ("AAPL", "SMART", "USD")
    assert (
        amsterdam.symbol,
        amsterdam.exchange,
        amsterdam.primaryExchange,
        amsterdam.currency,
    ) == (
        "ASML", "SMART", "AEB", "EUR"
    )
    assert (
        germany.symbol,
        germany.exchange,
        germany.primaryExchange,
        germany.currency,
    ) == (
        "SAP", "SMART", "IBIS", "EUR"
    )


def test_news_provider_parses_epoch_seconds_and_milliseconds():
    provider = IbkrNewsProvider()

    seconds = provider._parse_news_time("1721383200")
    milliseconds = provider._parse_news_time("1721383200000")

    assert seconds == milliseconds


def test_news_provider_parses_fractional_ibkr_datetime():
    provider = IbkrNewsProvider()

    parsed = provider._parse_news_time("2026-05-01 14:27:06.0")

    assert parsed.isoformat() == "2026-05-01T14:27:06+00:00"
