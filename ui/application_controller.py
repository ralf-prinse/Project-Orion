from PySide6.QtCore import QTimer

from providers.yahoo_provider import YahooProvider
from ui.foundation.dashboard_workspace_presenter import DashboardWorkspacePresenter
from ui.foundation.trading_workspace_presenter import TradingWorkspaceViewModel


class ApplicationController:
    """
    Central UI controller.

    Coordinates dashboard refresh, live dashboard updates,
    market scan and trading analysis.

    No trading decisions.
    No AI calculations.
    No rendering ownership.
    """

    LIVE_REFRESH_INTERVAL_MS = 60_000

    def __init__(self, dashboard_workspace, trading_workspace):
        self.dashboard_workspace = dashboard_workspace
        self.trading_workspace = trading_workspace

        self.dashboard_presenter = DashboardWorkspacePresenter()
        self.market_provider = YahooProvider()

        self.portfolio_state = None
        self.dashboard_symbol = "SPY"
        self.dashboard_period = "3mo"
        self.dashboard_interval = "1d"

        self.live_dashboard_enabled = False
        self.live_refresh_count = 0

        self.live_dashboard_timer = QTimer()
        self.live_dashboard_timer.setInterval(self.LIVE_REFRESH_INTERVAL_MS)
        self.live_dashboard_timer.timeout.connect(self.refresh_live_dashboard)

    def refresh_dashboard(self):
        workspace = self.dashboard_presenter.create_workspace(
            portfolio_state=self.portfolio_state,
            chart_title=f"{self.dashboard_symbol} Price Curve",
            chart_subtitle="Klik op Analyseer markt om actuele marktdata op te halen.",
            chart_values=[],
            chart_labels=[],
            symbol=self.dashboard_symbol,
            period_label="3 maanden",
            source_label="Yahoo Finance",
        )

        self.dashboard_workspace.set_workspace(workspace)

    def scan_ai_market(self):
        """
        User-triggered market scan.

        This starts the live dashboard refresh cycle after the first
        successful dashboard data request.
        """

        print(f"Market scan triggered for {self.dashboard_symbol}")

        self.live_dashboard_enabled = True
        self.live_refresh_count = 0

        self.refresh_live_dashboard()
        self._start_live_dashboard_timer()

    def refresh_live_dashboard(self):
        """
        Refresh dashboard market data from the configured provider.

        This is live dashboard orchestration only. The controller requests
        provider data and forwards presentation-safe values and labels to
        the presenter.

        It does not calculate trading decisions, indicators or AI output.
        """

        print(f"Live dashboard refresh for {self.dashboard_symbol}")

        chart_values, chart_labels = self._load_live_price_chart_data(
            self.dashboard_symbol
        )

        if chart_values:
            self.live_refresh_count += 1

        workspace = self.dashboard_presenter.create_workspace(
            portfolio_state=self.portfolio_state,
            chart_title=f"{self.dashboard_symbol} Price Curve",
            chart_subtitle=self._create_live_dashboard_subtitle(),
            chart_values=chart_values,
            chart_labels=chart_labels,
            symbol=self.dashboard_symbol,
            period_label="3 maanden",
            source_label="Yahoo Finance",
        )

        self.dashboard_workspace.set_workspace(workspace)

    def stop_live_dashboard(self):
        """
        Stop the live dashboard refresh cycle.
        """

        self.live_dashboard_enabled = False
        self.live_dashboard_timer.stop()

    def analyze_symbol(self, symbol: str):
        print(f"Analyzing {symbol}")

        view_model = TradingWorkspaceViewModel(
            decision="HOLD",
            decision_reason=f"Mock analysis for {symbol}",
            confidence="67%",
            confidence_subtitle="Medium confidence",
            pressure_score="45",
            pressure_subtitle="Neutral pressure",
            position_size="Medium",
            position_subtitle="Balanced sizing",
            risk_score="Low",
            risk_subtitle="Controlled risk",
            explanation=f"AI mock explanation for {symbol}",
            status="Analyse voltooid",
        )

        self.trading_workspace.set_view_model(view_model)

    def _start_live_dashboard_timer(self):
        if not self.live_dashboard_timer.isActive():
            self.live_dashboard_timer.start()

    def _create_live_dashboard_subtitle(self) -> str:
        interval_seconds = int(self.LIVE_REFRESH_INTERVAL_MS / 1000)

        if not self.live_dashboard_enabled:
            return "Laatste scan-data uit Yahoo Finance."

        if self.live_refresh_count <= 1:
            return (
                "Auto-refresh actief • Yahoo Finance close-prijzen • "
                f"ververst elke {interval_seconds} seconden"
            )

        return (
            "Auto-refresh actief • Yahoo Finance close-prijzen • "
            f"ververst elke {interval_seconds} seconden • "
            f"updates: {self.live_refresh_count}"
        )

    def _load_live_price_chart_data(self, symbol: str) -> tuple[list[float], list[str]]:
        try:
            history = self.market_provider.get_historical_data(
                symbol=symbol,
                period=self.dashboard_period,
                interval=self.dashboard_interval,
            )

            close_series = history["Close"].dropna()

            values = [float(value) for value in close_series.tolist()]
            labels = [
                self._format_market_date(index_value)
                for index_value in close_series.index.tolist()
            ]

            return values, labels

        except Exception as error:
            print(f"Live market data error: {error}")
            return [], []

    def _format_market_date(self, value) -> str:
        try:
            return value.strftime("%Y-%m-%d")
        except AttributeError:
            return str(value)