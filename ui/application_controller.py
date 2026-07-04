from providers.yahoo_provider import YahooProvider
from ui.foundation.dashboard_workspace_presenter import DashboardWorkspacePresenter
from ui.foundation.trading_workspace_presenter import TradingWorkspaceViewModel


class ApplicationController:
    """
    Central UI controller.

    Coordinates dashboard refresh, market scan and trading analysis.

    No trading decisions.
    No AI calculations.
    """

    def __init__(self, dashboard_workspace, trading_workspace):
        self.dashboard_workspace = dashboard_workspace
        self.trading_workspace = trading_workspace

        self.dashboard_presenter = DashboardWorkspacePresenter()
        self.market_provider = YahooProvider()

        self.portfolio_state = None
        self.dashboard_symbol = "SPY"

    def refresh_dashboard(self):
        workspace = self.dashboard_presenter.create_workspace(
            portfolio_state=self.portfolio_state,
            chart_title=f"{self.dashboard_symbol} Price Curve",
            chart_subtitle="Klik op Analyseer markt om live marktdata op te halen.",
            chart_values=[],
        )

        self.dashboard_workspace.set_workspace(workspace)

    def scan_ai_market(self):
        print(f"Market scan triggered for {self.dashboard_symbol}")

        chart_values = self._load_live_close_prices(self.dashboard_symbol)

        workspace = self.dashboard_presenter.create_workspace(
            portfolio_state=self.portfolio_state,
            chart_title=f"{self.dashboard_symbol} Live Price Curve",
            chart_subtitle="Live Yahoo Finance close-prijzen.",
            chart_values=chart_values,
        )

        self.dashboard_workspace.set_workspace(workspace)

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

    def _load_live_close_prices(self, symbol: str) -> list[float]:
        try:
            history = self.market_provider.get_historical_data(
                symbol=symbol,
                period="3mo",
                interval="1d",
            )

            closes = history["Close"].dropna().tolist()

            return [float(value) for value in closes]

        except Exception as error:
            print(f"Live market data error: {error}")
            return []