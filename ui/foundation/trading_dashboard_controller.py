from __future__ import annotations

from models.live_paper_trading_config import LivePaperTradingConfig
from services.dashboard_service import DashboardService
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)
from ui.foundation.trading_dashboard_gui_presenter import (
    TradingDashboardGuiPresenter,
)
from ui.workspace.trading_dashboard_workspace import (
    TradingDashboardWorkspace,
)


class TradingDashboardController:
    """
    Controller for the Trading Dashboard GUI.

    Responsibilities:
    - load runtime paper trading data
    - call DashboardService
    - call TradingDashboardGuiPresenter
    - update TradingDashboardWorkspace

    Does NOT:
    - calculate dashboard statistics
    - make trading decisions
    - modify portfolio state
    - render widgets directly
    """

    def __init__(
        self,
        workspace: TradingDashboardWorkspace,
        portfolio_repository: JsonPaperPortfolioRepository | None = None,
        trade_journal_repository: JsonlTradeJournalRepository | None = None,
        decision_journal_repository: (
            JsonlTradeJournalRepository | None
        ) = None,
        dashboard_service: DashboardService | None = None,
        presenter: TradingDashboardGuiPresenter | None = None,
        config: LivePaperTradingConfig | None = None,
    ):
        self.workspace = workspace
        self.portfolio_repository = (
            portfolio_repository
            or JsonPaperPortfolioRepository(
                path="data/paper_portfolio.json",
            )
        )
        self.trade_journal_repository = (
            trade_journal_repository
            or JsonlTradeJournalRepository(
                path="data/trade_journal.jsonl",
            )
        )
        self.decision_journal_repository = (
            decision_journal_repository
            or JsonlTradeJournalRepository(
                path="data/decision_journal.jsonl",
            )
        )
        self.dashboard_service = dashboard_service or DashboardService()
        self.presenter = presenter or TradingDashboardGuiPresenter()
        self.config = config or LivePaperTradingConfig()

    def refresh(self) -> None:
        if not self.portfolio_repository.exists():
            self.workspace.set_status_text(
                "Geen paper portfolio gevonden. Start eerst de paper trading runner."
            )
            return

        portfolio = self.portfolio_repository.load()
        journal_entries = self.trade_journal_repository.load_all()
        decision_entries = (
            self.decision_journal_repository.load_all()
        )

        snapshot = self.dashboard_service.build(
            portfolio=portfolio,
            journal_entries=journal_entries,
            initial_cash=self.config.initial_cash,
            decision_journal_entries=decision_entries,
        )

        workspace_model = self.presenter.create_workspace(
            snapshot=snapshot,
            recent_trades=journal_entries,
        )

        self.workspace.set_workspace(workspace_model)
