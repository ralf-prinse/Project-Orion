from datetime import datetime

from models.closed_trade_statistics import ClosedTradeStatistics
from models.paper_portfolio import PaperPortfolio
from models.trade_journal_entry import TradeJournalEntry
from services.dashboard_service import DashboardSnapshot
from ui.foundation.trading_dashboard_controller import TradingDashboardController
from ui.foundation.workspace import GuiWorkspace


class FakePortfolioRepository:
    def __init__(self, exists=True):
        self._exists = exists

    def exists(self):
        return self._exists

    def load(self):
        return PaperPortfolio(
            cash=500.0,
            positions={},
        )


class FakeTradeJournalRepository:
    def load_all(self):
        return [
            TradeJournalEntry(
                timestamp=datetime(2026, 7, 9, 12, 0, 0),
                symbol="AAA",
                action="OPEN_POSITION",
                decision="BUY",
                confidence=1.0,
                score=0.0,
                entry_price=100.0,
                exit_price=None,
                quantity=1,
                invested_amount=100.0,
                realized_profit_loss=0.0,
                unrealized_profit_loss=0.0,
                expected_risk=0.0,
                regime="UNKNOWN",
                volatility="UNKNOWN",
                ai_summary="Controller test.",
                recommendation_reason="Regression test.",
                cycle_number=1,
                session_id="test-session",
            )
        ]


class FakeDashboardService:
    def build(
        self,
        portfolio,
        journal_entries,
        initial_cash,
    ):
        return DashboardSnapshot(
            cash=500.0,
            equity=500.0,
            open_positions=0,
            open_profit_loss=0.0,
            closed_profit_loss=0.0,
            total_profit_loss=0.0,
            total_return_percent=0.0,
            closed_trades=0,
            winning_trades=0,
            losing_trades=0,
            winrate_percent=0.0,
            positions=[],
            closed_trade_statistics=ClosedTradeStatistics(
                closed_trades=0,
                winning_trades=0,
                losing_trades=0,
                winrate_percent=0.0,
                closed_profit_loss=0.0,
                average_winner=0.0,
                average_loser=0.0,
                profit_factor=0.0,
                largest_winner=0.0,
                largest_loser=0.0,
            ),
        )


class FakePresenter:
    def create_workspace(
        self,
        snapshot,
        recent_trades,
    ):
        return GuiWorkspace(
            title="Trading Dashboard",
            subtitle="Controller test workspace.",
            panels=[],
            metadata={},
        )


class FakeWorkspace:
    def __init__(self):
        self.status_text = None
        self.workspace = None

    def set_status_text(self, text):
        self.status_text = text

    def set_workspace(self, workspace):
        self.workspace = workspace


def test_trading_dashboard_controller_sets_status_when_portfolio_missing():
    workspace = FakeWorkspace()

    controller = TradingDashboardController(
        workspace=workspace,
        portfolio_repository=FakePortfolioRepository(exists=False),
        trade_journal_repository=FakeTradeJournalRepository(),
        dashboard_service=FakeDashboardService(),
        presenter=FakePresenter(),
    )

    controller.refresh()

    assert workspace.status_text is not None
    assert "Geen paper portfolio gevonden" in workspace.status_text
    assert workspace.workspace is None


def test_trading_dashboard_controller_refreshes_workspace():
    workspace = FakeWorkspace()

    controller = TradingDashboardController(
        workspace=workspace,
        portfolio_repository=FakePortfolioRepository(exists=True),
        trade_journal_repository=FakeTradeJournalRepository(),
        dashboard_service=FakeDashboardService(),
        presenter=FakePresenter(),
    )

    controller.refresh()

    assert workspace.status_text is None
    assert workspace.workspace is not None
    assert workspace.workspace.title == "Trading Dashboard"


def main():
    print("\n=========================================")
    print("ORION TRADING DASHBOARD CONTROLLER TEST")
    print("=========================================\n")

    test_trading_dashboard_controller_sets_status_when_portfolio_missing()
    test_trading_dashboard_controller_refreshes_workspace()

    print("TRADING DASHBOARD CONTROLLER: PASS ✅")


if __name__ == "__main__":
    main()