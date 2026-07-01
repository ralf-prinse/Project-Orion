from services.performance.models import PerformanceResult
from ui.foundation.performance_presenter import PerformancePresenter


def test_performance_presenter_creates_three_sections():
    presenter = PerformancePresenter()
    result = PerformanceResult(total_trades=10)

    sections = presenter.create_sections(result)

    assert [section.title for section in sections] == [
        "Trade Statistics",
        "Profitability",
        "Equity & Drawdown",
    ]


def test_performance_presenter_formats_profitability_metrics_deterministically():
    presenter = PerformancePresenter()
    result = PerformanceResult(
        gross_profit=1200.123,
        gross_loss=-500.456,
        net_pnl=699.667,
        profit_factor=2.399,
        expectancy=69.9667,
    )

    profitability = presenter.create_sections(result)[1]

    assert [metric.value for metric in profitability.metrics] == [
        "1200.12",
        "-500.46",
        "699.67",
        "2.40",
        "69.97",
    ]


def test_performance_presenter_formats_equity_metrics():
    presenter = PerformancePresenter()
    result = PerformanceResult(
        starting_equity=10000,
        ending_equity=11250.5,
        total_return_pct=12.505,
        max_drawdown_pct=4.334,
    )

    equity = presenter.create_sections(result)[2]

    assert [metric.value for metric in equity.metrics] == [
        "10000.00",
        "11250.50",
        "12.51%",
        "4.33%",
    ]
