from services.portfolio.models import (
    PortfolioPosition,
    PortfolioResult,
    PortfolioState,
)
from ui.foundation.portfolio_presenter import PortfolioPresenter


def test_portfolio_presenter_builds_account_and_position_sections():
    state = PortfolioState(
        cash=5000.0,
        positions={
            "MSFT": PortfolioPosition(
                symbol="MSFT",
                quantity=5,
                average_price=300.0,
                current_price=310.0,
                sector="Technology",
            ),
            "AAPL": PortfolioPosition(
                symbol="AAPL",
                quantity=10,
                average_price=150.0,
                current_price=155.0,
            ),
        },
    )

    sections = PortfolioPresenter().create_sections(state)
    titles = [section.title for section in sections]

    assert titles == ["Portfolio Account", "Open Positions"]
    assert sections[0].metrics[0].value == "5000.00"
    assert sections[0].metrics[1].value == "3100.00"
    assert sections[0].metrics[2].value == "8100.00"
    assert sections[1].metrics[0].value == "2"
    assert sections[1].metrics[1].label == "AAPL Quantity"
    assert sections[1].metrics[1].value == "10"
    assert any(metric.label == "MSFT Sector" and metric.value == "Technology" for metric in sections[1].metrics)


def test_portfolio_presenter_reports_empty_positions_without_calculating_trades():
    state = PortfolioState(cash=10000.0)

    sections = PortfolioPresenter().create_sections(state)

    assert sections[1].title == "Open Positions"
    assert sections[1].metrics[0].label == "Positions"
    assert sections[1].metrics[0].value == "0"


def test_portfolio_presenter_can_include_validation_result():
    state = PortfolioState(cash=1000.0)
    result = PortfolioResult(
        symbol="NVDA",
        portfolio_allowed=False,
        cash_sufficient=False,
        exposure_allowed=False,
        proposed_position_value=2500.0,
        position_exposure=0.5,
        total_exposure=1.1,
    )
    result.add_reason("Portfolio validation blocked proposal; insufficient cash available.")
    result.add_warning("Portfolio validation blocked proposal; total exposure limit exceeded.")

    sections = PortfolioPresenter().create_sections(
        portfolio_state=state,
        portfolio_result=result,
    )

    assert sections[2].title == "Portfolio Validation"
    assert sections[2].metrics[0].value == "NVDA"
    assert sections[2].metrics[1].value == "No"
    assert sections[2].metrics[2].value == "No"
    assert sections[2].metrics[6].value == "0.5000"
    assert sections[2].metrics[8].value == "2500.00"
    assert sections[2].metrics[-2].label == "Reason 1"
    assert sections[2].metrics[-1].label == "Warning 1"
