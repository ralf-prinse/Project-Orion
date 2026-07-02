from services.portfolio.models import PortfolioPosition, PortfolioState
from ui.foundation.portfolio_workspace_presenter import PortfolioWorkspacePresenter


def test_portfolio_workspace_presenter_creates_workspace_with_cards_and_sections():
    presenter = PortfolioWorkspacePresenter()

    state = PortfolioState(
        cash=500.0,
        currency="USD",
        positions={
            "AAPL": PortfolioPosition(
                symbol="AAPL",
                quantity=10,
                average_price=100.0,
                current_price=110.0,
            )
        },
    )

    workspace = presenter.create_workspace(state)

    card_titles = [card.title for card in workspace.cards]
    section_titles = [section.title for section in workspace.sections]

    assert "Totale waarde" in card_titles
    assert "Cash" in card_titles
    assert "Exposure" in card_titles
    assert "Open posities" in card_titles

    assert "Portfolio Analytics" in section_titles
    assert "Position Analytics" in section_titles
    assert "Portfolio Account" in section_titles
    assert "Open Positions" in section_titles


def test_portfolio_workspace_presenter_handles_empty_portfolio():
    presenter = PortfolioWorkspacePresenter()

    state = PortfolioState(
        cash=1000.0,
        currency="USD",
        positions={},
    )

    workspace = presenter.create_workspace(state)

    card_titles = [card.title for card in workspace.cards]
    section_titles = [section.title for section in workspace.sections]

    assert "Totale waarde" in card_titles
    assert "Cash" in card_titles
    assert "Exposure" in card_titles
    assert "Open posities" in card_titles

    assert "Portfolio Analytics" in section_titles
    assert "Position Analytics" in section_titles
    assert "Portfolio Account" in section_titles
    assert "Open Positions" in section_titles