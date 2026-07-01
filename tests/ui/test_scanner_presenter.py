from types import SimpleNamespace

from ui.foundation.scanner_presenter import ScannerPresenter


def test_scanner_presenter_builds_display_sections_from_scan_result():
    status = SimpleNamespace(
        universe_count=100,
        quotes_count=80,
        after_price_filter=70,
        after_volume_filter=60,
        after_liquidity_filter=50,
        after_relative_strength_filter=40,
        after_momentum_filter=30,
        technical_candidates_count=20,
        technical_results_count=10,
        opportunities_count=1,
        market_data_provider="MockProvider",
        total_seconds=1.23456,
        messages=[],
    )
    result = SimpleNamespace(
        opportunities=[
            SimpleNamespace(
                symbol="AAPL",
                action="BUY",
                confidence=88.5,
                reason="Strong deterministic setup",
            )
        ],
        status=status,
    )

    sections = ScannerPresenter().create_sections(result)
    titles = [section.title for section in sections]

    assert titles == [
        "Scanner Summary",
        "Scanner Pipeline",
        "Scanner Runtime",
        "Top Opportunities",
    ]
    assert sections[0].metrics[0].value == "100"
    assert sections[2].metrics[0].value == "MockProvider"
    assert sections[3].metrics[0].value == "AAPL"
    assert sections[3].metrics[2].value == "88.50"


def test_scanner_presenter_reports_empty_opportunities_without_calculating():
    status = SimpleNamespace(
        universe_count=10,
        quotes_count=0,
        quote_missing=10,
        provider_missing_quotes=10,
        messages=["Geen quote-data ontvangen."],
    )
    result = SimpleNamespace(opportunities=[], status=status)

    sections = ScannerPresenter().create_sections(result)
    titles = [section.title for section in sections]

    assert "Top Opportunities" in titles
    assert "Scanner Diagnostics" in titles
    assert sections[3].metrics[0].value == "None"
    assert sections[-1].metrics[0].label == "Missing Quotes"
    assert sections[-1].metrics[-1].value == "Geen quote-data ontvangen."
