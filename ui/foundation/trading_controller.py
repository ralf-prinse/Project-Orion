from __future__ import annotations

from providers.yahoo_provider import YahooProvider
from services.intelligence.indicator_builder import IndicatorBuilder
from services.orchestration.trading_pipeline import TradingPipeline
from ui.foundation.trading_workspace_presenter import TradingWorkspacePresenter


class TradingController:
    """
    Controller for the Trading Workspace.

    Responsibilities:
        - load historical market data
        - build deterministic IndicatorPack
        - execute TradingPipeline
        - transform pipeline output through TradingWorkspacePresenter
        - update TradingWorkspace

    No trading decisions are made here.
    No indicator calculations are implemented here.
    No AI logic is implemented here.
    No rendering ownership.
    """

    def __init__(
        self,
        trading_workspace,
        portfolio_state,
        market_provider: YahooProvider | None = None,
        indicator_builder: IndicatorBuilder | None = None,
        trading_pipeline: TradingPipeline | None = None,
        trading_presenter: TradingWorkspacePresenter | None = None,
    ) -> None:
        self.trading_workspace = trading_workspace
        self.portfolio_state = portfolio_state

        self.market_provider = market_provider or YahooProvider()
        self.indicator_builder = indicator_builder or IndicatorBuilder()
        self.trading_pipeline = trading_pipeline or TradingPipeline()
        self.trading_presenter = trading_presenter or TradingWorkspacePresenter()

        self.analysis_period = "6mo"
        self.analysis_interval = "1d"

    def analyze_symbol(self, symbol: str) -> None:
        normalized_symbol = symbol.strip().upper()

        if not normalized_symbol:
            self.trading_workspace.set_status_text("Vul eerst een symbool in.")
            return

        self.trading_workspace.set_status_text(
            f"Analyse gestart voor {normalized_symbol}..."
        )

        try:
            history = self.market_provider.get_historical_data(
                symbol=normalized_symbol,
                period=self.analysis_period,
                interval=self.analysis_interval,
            )

            indicator_pack = self.indicator_builder.build(
                symbol=normalized_symbol,
                history=history,
            )

            pipeline_result = self.trading_pipeline.run(
                indicator_data=indicator_pack,
                portfolio_state=self.portfolio_state,
            )

            view_model = self.trading_presenter.create_view_model(
                pipeline_result
            )

            self.trading_workspace.set_view_model(view_model)

        except Exception as error:
            self.trading_workspace.set_status_text(
                f"Analyse mislukt voor {normalized_symbol}: {error}"
            )