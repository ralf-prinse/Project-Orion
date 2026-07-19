from __future__ import annotations

from models.live_paper_trading_config import LivePaperTradingConfig
from services.dashboard_service import DashboardService
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)
from presentation.trading_dashboard_cli_presenter import (
    TradingDashboardCliPresenter,
)


def main() -> None:
    config = LivePaperTradingConfig()

    portfolio_repository = JsonPaperPortfolioRepository(
        path="data/paper_portfolio.json",
    )

    trade_journal_repository = JsonlTradeJournalRepository(
        path="data/trade_journal.jsonl",
    )

    decision_journal_repository = JsonlTradeJournalRepository(
        path="data/decision_journal.jsonl",
    )

    if not portfolio_repository.exists():
        print("No paper portfolio found.")
        print("Run paper trading first:")
        print("python run_continuous_paper_trading.py")
        return

    portfolio = portfolio_repository.load()
    journal_entries = trade_journal_repository.load_all()
    decision_entries = decision_journal_repository.load_all()

    snapshot = DashboardService().build(
        portfolio=portfolio,
        journal_entries=journal_entries,
        initial_cash=config.initial_cash,
        decision_journal_entries=decision_entries,
    )

    output = TradingDashboardCliPresenter().present(
        snapshot=snapshot,
        recent_trades=journal_entries,
    )

    print(output)


if __name__ == "__main__":
    main()
