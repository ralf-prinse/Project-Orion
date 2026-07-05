from models.trade_lifecycle import Trade
from services.position_monitor_service import PositionMonitorService
from ui.foundation.position_monitor_presenter import PositionMonitorPresenter


class PositionMonitorController:
    """
    Controller for the Position Monitor workspace.

    Responsibilities:
    - receive a Trade from the workspace;
    - invoke PositionMonitorService;
    - invoke PositionMonitorPresenter;
    - update the workspace.

    No business logic.
    No AI.
    No rendering logic.
    """

    def __init__(
        self,
        workspace,
        monitor_service: PositionMonitorService | None = None,
        presenter: PositionMonitorPresenter | None = None,
    ):
        self.workspace = workspace
        self.monitor_service = monitor_service or PositionMonitorService()
        self.presenter = presenter or PositionMonitorPresenter()

    def monitor_trade(self, trade: Trade) -> None:
        try:
            result = self.monitor_service.evaluate(trade)
            view_model = self.presenter.present(result)
            self.workspace.set_view_model(view_model)
        except Exception as error:
            self.workspace.set_status_text(
                f"Position Monitor mislukt: {error}"
            )