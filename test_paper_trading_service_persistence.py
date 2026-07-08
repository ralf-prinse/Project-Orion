from pathlib import Path

from models.paper_portfolio import PaperPortfolio
from services.paper_trading_service import PaperTradingService
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)


class DummyExecutionEngine:
    def execute(self, context):
        return type(
            "ExecutionResult",
            (),
            {
                "portfolio": context.portfolio,
                "execution": type(
                    "Execution",
                    (),
                    {
                        "accepted": False,
                        "message": "Rejected",
                    },
                )(),
            },
        )()


def test_repository_is_used_after_trade():
    path = Path("output/test_service_portfolio.json")

    repository = JsonPaperPortfolioRepository(
        path=path,
    )

    repository.delete()

    service = PaperTradingService(
        execution_engine=DummyExecutionEngine(),
        portfolio_repository=repository,
    )

    # We simuleren alleen de save-stap.
    repository.save(
        PaperPortfolio(
            cash=123.45,
        )
    )

    assert repository.exists()

    restored = repository.load()

    assert restored.cash == 123.45

    repository.delete()