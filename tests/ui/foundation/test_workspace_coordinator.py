from models.portfolio import Portfolio, Position
from ui.foundation.workspace_coordinator import WorkspaceCoordinator


def test_workspace_coordinator_creates_portfolio_workspace():
    coordinator = WorkspaceCoordinator()

    portfolio = Portfolio(
        cash=500.0,
        currency="USD",
        positions={
            "AAPL": Position(
                symbol="AAPL",
                quantity=10,
                average_price=100.0,
                currency="USD",
            )
        },
    )

    workspace = coordinator.create_portfolio_workspace(portfolio)

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