from models.trade_lifecycle import Trade
from services.position_analysis_service import PositionAnalysisService
from services.position_monitor_service import PositionMonitorService
from ui.foundation.position_monitor_presenter import PositionMonitorPresenter


class PositionMonitorController:
    """
    Controller for the Position Monitor workspace.

    Responsibilities
    ----------------
    - receive a Trade from the workspace
    - retrieve latest technical analysis
    - invoke PositionMonitorService
    - invoke PositionMonitorPresenter
    - update the workspace

    No business logic.
    No AI.
    No rendering.
    """

    def __init__(
        self,
        workspace,
        analysis_service: PositionAnalysisService | None = None,
        monitor_service: PositionMonitorService | None = None,
        presenter: PositionMonitorPresenter | None = None,
    ):
        self.workspace = workspace

        self.analysis_service = (
            analysis_service or PositionAnalysisService()
        )

        self.monitor_service = (
            monitor_service or PositionMonitorService()
        )

        self.presenter = (
            presenter or PositionMonitorPresenter()
        )

    def monitor_trade(
        self,
        trade: Trade,
    ) -> None:
        try:
            self.workspace.set_status_text(
                f"Technische analyse ophalen voor {trade.symbol}..."
            )

            analysis = self.analysis_service.analyze_position(
                trade.symbol
            )

            result = self.monitor_service.evaluate(
                trade=trade,
                analysis=analysis,
            )

            view_model = self.presenter.present(result)

            self.workspace.set_view_model(view_model)

        except Exception as error:
            self.workspace.set_status_text(
                f"Position Monitor mislukt: {error}"
            )