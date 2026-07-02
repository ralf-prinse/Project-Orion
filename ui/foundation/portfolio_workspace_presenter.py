from services.portfolio.analytics_service import PortfolioAnalyticsService
from services.portfolio.models import PortfolioState
from ui.foundation.models import GuiWorkspace
from ui.foundation.portfolio_analytics_presenter import PortfolioAnalyticsPresenter
from ui.foundation.portfolio_metric_card_presenter import PortfolioMetricCardPresenter
from ui.foundation.portfolio_presenter import PortfolioPresenter


class PortfolioWorkspacePresenter:
    """
    Composes the complete Portfolio workspace presentation model.

    This presenter coordinates portfolio display sections, analytics sections
    and KPI cards. It performs no portfolio calculations itself.
    """

    def __init__(
        self,
        portfolio_presenter: PortfolioPresenter | None = None,
        analytics_service: PortfolioAnalyticsService | None = None,
        analytics_presenter: PortfolioAnalyticsPresenter | None = None,
        metric_card_presenter: PortfolioMetricCardPresenter | None = None,
    ):
        self.portfolio_presenter = portfolio_presenter or PortfolioPresenter()
        self.analytics_service = analytics_service or PortfolioAnalyticsService()
        self.analytics_presenter = analytics_presenter or PortfolioAnalyticsPresenter()
        self.metric_card_presenter = (
            metric_card_presenter or PortfolioMetricCardPresenter()
        )

    def create_workspace(self, portfolio_state: PortfolioState) -> GuiWorkspace:
        analytics_result = self.analytics_service.analyze(portfolio_state)

        cards = self.metric_card_presenter.create_cards(analytics_result)

        sections = [
            *self.analytics_presenter.create_sections(analytics_result),
            *self.portfolio_presenter.create_sections(portfolio_state),
        ]

        return GuiWorkspace(
            cards=cards,
            sections=sections,
        )