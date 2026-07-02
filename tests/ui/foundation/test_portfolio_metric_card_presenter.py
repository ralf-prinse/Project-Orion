from services.portfolio.analytics_models import PortfolioAnalyticsResult
from ui.foundation.portfolio_metric_card_presenter import PortfolioMetricCardPresenter


def test_portfolio_metric_card_presenter_creates_cards():
    presenter = PortfolioMetricCardPresenter()

    result = PortfolioAnalyticsResult(
        cash=500.0,
        invested_value=1500.0,
        total_value=2000.0,
        open_positions=3,
        total_exposure=0.75,
        average_position_value=500.0,
        largest_position_symbol="AAPL",
        largest_position_value=900.0,
        currency="USD",
    )

    cards = presenter.create_cards(result)

    assert len(cards) == 4

    assert cards[0].title == "Totale waarde"
    assert cards[0].value == "USD 2000.00"

    assert cards[1].title == "Cash"
    assert cards[1].value == "USD 500.00"

    assert cards[2].title == "Exposure"
    assert cards[2].value == "75.00%"

    assert cards[3].title == "Open posities"
    assert cards[3].value == "3"