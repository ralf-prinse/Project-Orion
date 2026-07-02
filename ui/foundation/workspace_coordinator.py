from models.portfolio import Portfolio

from services.portfolio.portfolio_state_adapter import PortfolioStateAdapter

from ui.foundation.portfolio_workspace_presenter import PortfolioWorkspacePresenter
from ui.foundation.performance_workspace_presenter import PerformanceWorkspacePresenter


class WorkspaceCoordinator:
    """
    Central routing layer for all UI workspaces.

    Responsibilities:
    - convert domain models → workspace presenters
    - route workspace selection
    - keep MainWindow clean
    """

    def __init__(
        self,
        portfolio_state_adapter: PortfolioStateAdapter | None = None,
        portfolio_workspace_presenter: PortfolioWorkspacePresenter | None = None,
        performance_workspace_presenter: PerformanceWorkspacePresenter | None = None,
    ):
        self.portfolio_state_adapter = (
            portfolio_state_adapter or PortfolioStateAdapter()
        )

        self.portfolio_workspace_presenter = (
            portfolio_workspace_presenter or PortfolioWorkspacePresenter()
        )

        # NEW: Performance workspace
        self.performance_workspace_presenter = (
            performance_workspace_presenter or PerformanceWorkspacePresenter()
        )

    # -----------------------------------------
    # PORTFOLIO WORKSPACE
    # -----------------------------------------
    def create_portfolio_workspace(self, portfolio: Portfolio):
        portfolio_state = self.portfolio_state_adapter.from_portfolio(portfolio)

        return self.portfolio_workspace_presenter.create_workspace(
            portfolio_state
        )

    # -----------------------------------------
    # PERFORMANCE WORKSPACE (NEW)
    # -----------------------------------------
    def create_performance_workspace(self, portfolio: Portfolio):
        """
        Returns performance + benchmark dashboard workspace
        """

        portfolio_state = self.portfolio_state_adapter.from_portfolio(portfolio)

        return self.performance_workspace_presenter.create_workspace(
            portfolio_state
        )

    # -----------------------------------------
    # ROUTING
    # -----------------------------------------
    def get_workspace(self, name: str, portfolio: Portfolio):
        """
        Main routing entry point for UI
        """

        if name == "portfolio":
            return self.create_portfolio_workspace(portfolio)

        if name == "performance":
            return self.create_performance_workspace(portfolio)

        raise ValueError(f"Unknown workspace: {name}")