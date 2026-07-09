from __future__ import annotations

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)


def main():
    portfolio_repository = JsonPaperPortfolioRepository(
        path="data/paper_portfolio.json",
    )

    trade_journal_repository = JsonlTradeJournalRepository(
        path="data/trade_journal.jsonl",
    )

    autonomous_config = AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=500.0,
            max_symbols=25,
        ),
        print_cycle_summary=True,
    )

    autonomous_runner = AutonomousPaperTradingRunner(
        config=autonomous_config,
        portfolio_repository=portfolio_repository,
        trade_journal_repository=trade_journal_repository,
    )

    config = ContinuousRunnerConfig(
        autonomous_config=autonomous_config,
        interval_seconds=300,
        max_iterations=None,
        stop_on_exception=False,
        print_iteration_summary=True,
    )

    runner = ContinuousPaperTradingRunner(
        config=config,
        runner=autonomous_runner,
    )

    print("\n=========================================")
    print("ORION CONTINUOUS PAPER TRADING")
    print("=========================================")
    print("Press Ctrl+C to stop.")
    print("Interval: 300 seconds")
    print("Portfolio: data/paper_portfolio.json")
    print("Trade journal: data/trade_journal.jsonl")
    print("=========================================\n")

    result = runner.run()

    print("\n=========================================")
    print("CONTINUOUS PAPER TRADING STOPPED")
    print("=========================================")
    print(f"Iterations completed: {result.iterations_completed}")
    print(f"Failed iterations:    {result.failed_iterations}")

    if result.last_result is not None:
        print(f"Final cash:           €{result.last_result.final_cash:.2f}")
        print(f"Final equity:         €{result.last_result.final_equity:.2f}")
        print(
            "Open positions:       "
            f"{len(result.last_result.session.portfolio.positions)}"
        )

    print("=========================================\n")


if __name__ == "__main__":
    main()