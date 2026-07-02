from models.portfolio import Portfolio
from services.portfolio.portfolio_state_adapter import PortfolioStateAdapter
from ui.foundation.models import GuiWorkspace
from ui.foundation.portfolio_workspace_presenter import PortfolioWorkspacePresenter


class WorkspaceCoordinator:
    """
    Coordinates workspace-level presentation models.

    MainWindow remains the composition root, but does not compose workspace
    presentation details itself. This coordinator delegates to workspace
    presenters and keeps orchestration small and explicit.
    """

    def __init__(
        self,
        portfolio_state_adapter: PortfolioStateAdapter | None = None,
        portfolio_workspace_presenter: PortfolioWorkspacePresenter | None = None,
    ):
        self.portfolio_state_adapter = (
            portfolio_state_adapter or PortfolioStateAdapter()
        )
        self.portfolio_workspace_presenter = (
            portfolio_workspace_presenter or PortfolioWorkspacePresenter()
        )

    def create_portfolio_workspace(
        self,
        portfolio: Portfolio,
    ) -> GuiWorkspace:
        """
        Build the complete Portfolio workspace presentation model.
        """

        portfolio_state = self.portfolio_state_adapter.from_portfolio(portfolio)

        workspace = self.portfolio_workspace_presenter.create_workspace(
            portfolio_state
        )

        print("=" * 60)
        print("Portfolio workspace debug")
        print(f"Cash      : {portfolio_state.cash}")
        print(f"Positions : {len(portfolio_state.positions)}")
        print(f"Cards     : {len(workspace.cards)}")
        print(f"Sections  : {len(workspace.sections)}")
        print("=" * 60)

        return workspace