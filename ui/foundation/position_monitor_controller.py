from models.trade_lifecycle import Trade
from services.open_trade_store import OpenTradeStore
from services.position_analysis_service import PositionAnalysisService
from services.position_monitor_service import PositionMonitorService
from services.trade_history_store import TradeHistoryStore
from services.trade_lifecycle_service import TradeLifecycleService
from services.trade_monitor_service import TradeMonitorService
from ui.foundation.position_monitor_presenter import PositionMonitorPresenter
from ui.foundation.trade_monitor_presenter import TradeMonitorPresenter


class PositionMonitorController:
    """
    Controller for the Trade Monitor workspace.

    Responsibilities
    ----------------
    - receive manual Trade input from the workspace
    - retrieve latest technical analysis
    - invoke PositionMonitorService
    - invoke PositionMonitorPresenter
    - load persisted open trades
    - refresh open trades
    - close open trades
    - invoke TradeMonitorPresenter
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
        trade_monitor_service: TradeMonitorService | None = None,
        trade_monitor_presenter: TradeMonitorPresenter | None = None,
        trade_lifecycle_service: TradeLifecycleService | None = None,
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

        self.trade_lifecycle_service = (
            trade_lifecycle_service
            or TradeLifecycleService(
                open_trade_store=OpenTradeStore(),
                trade_history_store=TradeHistoryStore(),
            )
        )

        self.trade_monitor_service = (
            trade_monitor_service
            or TradeMonitorService(
                trade_lifecycle_service=self.trade_lifecycle_service,
            )
        )

        self.trade_monitor_presenter = (
            trade_monitor_presenter or TradeMonitorPresenter()
        )

    def load_open_trades(self) -> None:
        try:
            trades = self.trade_monitor_service.get_open_trades()
            view_model = self.trade_monitor_presenter.present_open_trades(
                trades
            )

            self.workspace.set_open_trades_view_model(view_model)
            self.workspace.set_open_trade_cards(trades)

        except Exception as error:
            self.workspace.set_status_text(
                f"Open trades laden mislukt: {error}"
            )

    def refresh_open_trades(self) -> None:
        """
        Refresh open trades and update the Open Trades panel.

        The controller only orchestrates:
        - service refreshes prices and P/L
        - service evaluates exit status
        - presenter formats the result
        - workspace renders the view model
        """

        try:
            trades = self.trade_monitor_service.refresh_and_evaluate_all()
            view_model = self.trade_monitor_presenter.present_open_trades(
                trades
            )

            self.workspace.set_open_trades_view_model(view_model)

        except Exception as error:
            self.workspace.set_status_text(
                f"Open trades verversen mislukt: {error}"
            )

    def close_trade(
        self,
        symbol: str,
        reason: str = "Handmatig gesloten via Trade Monitor.",
    ) -> None:
        normalized_symbol = str(symbol).strip().upper()

        if not normalized_symbol:
            self.workspace.set_status_text(
                "Close Trade mislukt: geen geldig symbool."
            )
            return

        try:
            open_trades = self.trade_lifecycle_service.get_open_trades()

            has_trade = any(
                trade.symbol.upper() == normalized_symbol
                for trade in open_trades
            )

            if not has_trade:
                self.workspace.set_status_text(
                    f"Geen open trade gevonden voor {normalized_symbol}."
                )
                return

            self.trade_lifecycle_service.close_trade(
                symbol=normalized_symbol,
                reason=reason,
            )

            self.load_open_trades()

            self.workspace.set_status_text(
                f"Trade gesloten voor {normalized_symbol}."
            )

        except Exception as error:
            self.workspace.set_status_text(
                f"Close Trade mislukt voor {normalized_symbol}: {error}"
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
                f"Trade Monitor mislukt: {error}"
            )