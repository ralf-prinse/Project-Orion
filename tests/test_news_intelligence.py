from __future__ import annotations

from datetime import UTC, datetime, timedelta

from models.news_event import RawNewsItem
from models.autonomous_paper_trading_config import AutonomousPaperTradingConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import (
    LivePaperCandidate,
    LivePaperTradingResult,
)
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.autonomous_paper_trading_runner import AutonomousPaperTradingRunner
from services.news.news_intelligence_service import NewsIntelligenceService
from services.news.news_normalizer import NewsNormalizer
from services.stores.jsonl_news_assessment_repository import (
    JsonlNewsAssessmentRepository,
)
from services.stores.jsonl_news_event_repository import JsonlNewsEventRepository


NOW = datetime(2026, 7, 19, 10, 0, tzinfo=UTC)


class FixedProvider:
    name = "TEST_NEWS"

    def __init__(self, items=(), error=None):
        self.items = tuple(items)
        self.error = error
        self.calls = []

    def fetch_recent(self, *, symbols, since, max_articles_per_symbol):
        self.calls.append((symbols, since, max_articles_per_symbol))
        if self.error is not None:
            raise self.error
        return self.items


def raw(headline, article_id="1", symbol="AAPL"):
    return RawNewsItem(
        provider="TEST_NEWS",
        article_id=article_id,
        headline=headline,
        published_at=NOW - timedelta(hours=1),
        symbols=(symbol,),
    )


def test_high_risk_news_is_observed_but_remains_shadow_only(tmp_path):
    provider = FixedProvider([raw("Company cuts guidance after data breach")])
    events = JsonlNewsEventRepository(tmp_path / "events.jsonl")
    assessments = JsonlNewsAssessmentRepository(tmp_path / "assessments.jsonl")
    service = NewsIntelligenceService(
        provider=provider,
        event_repository=events,
        assessment_repository=assessments,
        clock=lambda: NOW,
    )

    result = service.assess_symbols(("AAPL",))["AAPL"]

    assert result.mode == "SHADOW"
    assert result.status == "AVAILABLE"
    assert result.risk_level == "HIGH"
    assert result.blocking_recommended is True
    assert "did not alter trading behavior" in result.reasons[-1]
    assert len(events.load_all()) == 1
    assert len(assessments.load_all()) == 1


def test_duplicate_provider_items_are_persisted_once(tmp_path):
    duplicate = raw("Company raises guidance", article_id="same")
    repository = JsonlNewsEventRepository(tmp_path / "events.jsonl")
    service = NewsIntelligenceService(
        provider=FixedProvider([duplicate, duplicate]),
        event_repository=repository,
        clock=lambda: NOW,
    )

    service.assess_symbols(("AAPL",))
    service.assess_symbols(("AAPL",))

    assert len(repository.load_all()) == 1


def test_items_outside_lookback_window_are_ignored():
    stale = RawNewsItem(
        provider="TEST_NEWS",
        article_id="stale",
        headline="Company files for chapter 11",
        published_at=NOW - timedelta(hours=25),
        symbols=("AAPL",),
    )
    service = NewsIntelligenceService(
        provider=FixedProvider([stale]),
        lookback_hours=24,
        clock=lambda: NOW,
    )

    result = service.assess_symbols(("AAPL",))["AAPL"]

    assert result.status == "NO_NEWS"
    assert result.blocking_recommended is False


def test_provider_failure_is_fail_open_and_audited():
    service = NewsIntelligenceService(
        provider=FixedProvider(error=TimeoutError("offline")),
        clock=lambda: NOW,
    )

    result = service.assess_symbols(("ASML.AS",))["ASML.AS"]

    assert result.status == "UNAVAILABLE"
    assert result.blocking_recommended is False
    assert "TimeoutError" in result.reasons[0]
    assert result.reasons[-1] == "Trading behavior was not altered."


def test_normalizer_handles_european_and_us_symbols():
    event = NewsNormalizer().normalize(
        raw("ECB interest rate decision", symbol="ASML.AS"),
        received_at=NOW,
    )

    assert event.symbols == ("ASML.AS",)
    assert event.category == "MACRO"
    assert event.severity == "MEDIUM"
    assert event.published_at.tzinfo is UTC


def test_runner_shadow_enrichment_never_changes_candidate_decision():
    service = NewsIntelligenceService(
        provider=FixedProvider([raw("Company files for chapter 11")]),
        clock=lambda: NOW,
    )
    runner = AutonomousPaperTradingRunner(
        config=AutonomousPaperTradingConfig(
            live_config=LivePaperTradingConfig(news_mode="SHADOW")
        ),
        news_intelligence_service=service,
    )
    candidate = LivePaperCandidate(
        symbol="AAPL",
        result=object(),
        score=0.9,
        accepted=True,
        reason="Canonical technical decision accepted.",
    )
    scan = LivePaperTradingResult(
        session=TradingSession(
            name="shadow-test",
            portfolio=PaperPortfolio(cash=10_000.0),
        ),
        scanned_symbols=1,
        succeeded_symbols=1,
        failed_symbols=0,
        failed_symbol_errors={},
        scan_duration_seconds=0.1,
        candidates=[candidate],
        executed_trades=0,
        rejected_trades=0,
    )

    enriched = runner._enrich_scan_with_news(scan)

    assert enriched.candidates[0].accepted is True
    assert enriched.candidates[0].reason == candidate.reason
    assert enriched.candidates[0].news_assessment.blocking_recommended is True
