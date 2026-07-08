from pathlib import Path

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)


def test_save_and_load_repository():
    repository = JsonPaperPortfolioRepository(
        path=Path("output/test_paper_portfolio.json"),
    )

    repository.delete()

    portfolio = PaperPortfolio(
        cash=500.0,
        positions={
            "AAPL": PaperPosition(
                symbol="AAPL",
                quantity=2,
                entry_price=100.0,
                current_price=110.0,
            ),
        },
    )

    repository.save(portfolio)

    assert repository.exists()

    loaded = repository.load()

    assert loaded.cash == portfolio.cash
    assert loaded.positions.keys() == portfolio.positions.keys()

    position = loaded.positions["AAPL"]

    assert position.symbol == "AAPL"
    assert position.quantity == 2
    assert position.entry_price == 100.0
    assert position.current_price == 110.0

    repository.delete()

    assert not repository.exists()


def test_delete_non_existing_repository():
    repository = JsonPaperPortfolioRepository(
        path=Path("output/test_delete.json"),
    )

    repository.delete()

    assert repository.exists() is False