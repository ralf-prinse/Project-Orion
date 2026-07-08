from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)


class EmptyScanner:
    def run(self, session):
        return type(
            "ScanResult",
            (),
            {
                "candidates": [],
                "scanned_symbols": 0,
            },
        )()


def test_runner_loads_existing_portfolio():
    repository = JsonPaperPortfolioRepository(
        path="output/test_runner_portfolio.json",
    )

    repository.delete()

    repository.save(
        PaperPortfolio(
            cash=321.0,
        )
    )

    runner = AutonomousPaperTradingRunner(
        config=AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
            live_config=LivePaperTradingConfig(
                initial_cash=500.0,
            ),
        ),
        scanner=EmptyScanner(),
        portfolio_repository=repository,
    )

    result = runner.run()

    assert result.initial_cash == 500.0
    assert result.final_cash == 321.0
    assert result.final_equity == 321.0

    repository.delete()


def test_runner_saves_created_portfolio():
    repository = JsonPaperPortfolioRepository(
        path="output/test_runner_created_portfolio.json",
    )

    repository.delete()

    runner = AutonomousPaperTradingRunner(
        config=AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
            live_config=LivePaperTradingConfig(
                initial_cash=777.0,
            ),
        ),
        scanner=EmptyScanner(),
        portfolio_repository=repository,
    )

    result = runner.run()

    assert result.final_cash == 777.0
    assert repository.exists()

    restored = repository.load()

    assert restored.cash == 777.0

    repository.delete()