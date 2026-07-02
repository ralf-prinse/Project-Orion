from config.trading_config import DEFAULT_TRADING_CONFIG

from providers.yahoo_provider import YahooProvider

from services.intelligence.indicator_builder import IndicatorBuilder
from services.logging_service import LoggingService
from services.orchestration.ai_market_scanner import AIMarketScanner
from services.orchestration.trading_pipeline import TradingPipeline

from ui.foundation.ai_scanner_presenter import AIScannerPresenter
from ui.foundation.trading_workspace_presenter import TradingWorkspacePresenter


class ApplicationController:
    """
    Central application controller for Orion.

    Responsibilities
    ----------------
    - Connect UI actions to backend services
    - Keep MainWindow free of business logic
    - Coordinate Trading Workspace
    - Coordinate AI Scanner Workspace
    """

    def __init__(self, window):
        self.window = window

        self.logger = LoggingService.get_logger(
            "ApplicationController"
        )

        self.config = DEFAULT_TRADING_CONFIG

        self.provider = YahooProvider()

        self.indicator_builder = IndicatorBuilder(
            config=self.config.indicators
        )

        self.trading_pipeline = TradingPipeline()

        self.trading_presenter = TradingWorkspacePresenter()

        self.ai_market_scanner = AIMarketScanner(
            provider=self.provider,
            indicator_builder=self.indicator_builder,
            trading_pipeline=self.trading_pipeline,
        )

        self.ai_scanner_presenter = AIScannerPresenter()

    # ==========================================================
    # TRADING
    # ==========================================================

    def analyze_symbol(self, symbol: str):

        try:

            symbol = symbol.strip().upper()

            if not symbol:
                self.window.trading_page.set_status_text(
                    "Vul eerst een symbool in."
                )
                return

            self.logger.info(
                "User requested analysis for %s",
                symbol,
            )

            self.window.trading_page.set_status_text(
                f"Live marktdata ophalen voor {symbol}..."
            )

            history = self.provider.get_historical_data(
                symbol=symbol,
                period=self.config.market_data.history_period,
                interval=self.config.market_data.history_interval,
            )

            self.window.trading_page.set_status_text(
                f"Indicatoren berekenen voor {symbol}..."
            )

            indicators = self.indicator_builder.build(
                symbol=symbol,
                history=history,
            )

            self.window.trading_page.set_status_text(
                "Trading Pipeline uitvoeren..."
            )

            result = self.trading_pipeline.run(
                indicator_data=indicators,
                portfolio_state=self.window.portfolio,
            )

            view_model = self.trading_presenter.create_view_model(
                result
            )

            self.window.trading_page.set_view_model(
                view_model
            )

            self.window.trading_page.set_status_text(
                "Analyse voltooid."
            )

            pipeline = result["pipeline"]

            self.logger.info(
                (
                    "Analysis completed | %s | %s | "
                    "confidence=%.3f"
                ),
                pipeline["symbol"],
                pipeline["decision"],
                pipeline["confidence"],
            )

        except Exception as error:

            self.logger.exception(
                "Trading analysis failed: %s",
                error,
            )

            self.window.trading_page.set_status_text(
                f"Analyse mislukt: {error}"
            )

    # ==========================================================
    # AI MARKET SCANNER
    # ==========================================================

    def scan_ai_market(self):

        try:

            self.logger.info(
                "User started AI market scan"
            )

            self.window.dashboard_page.set_status_text(
                "AI Scanner analyseert markt..."
            )

            self.window.scanner_page.set_status_text(
                "AI Scanner analyseert markt..."
            )

            scan_result = self.ai_market_scanner.scan(
                symbols=self.config.scanner.default_symbols,
                portfolio_state=self.window.portfolio,
                period=self.config.market_data.history_period,
                interval=self.config.market_data.history_interval,
            )

            sections = self.ai_scanner_presenter.create_sections(
                scan_result=scan_result,
                max_items=self.config.scanner.max_results,
            )

            self.window.dashboard_page.set_sections(
                sections
            )

            self.window.scanner_page.set_sections(
                sections
            )

            self.window.dashboard_page.set_status_text(
                "AI Scanner analyse voltooid."
            )

            self.window.scanner_page.set_status_text(
                "AI Scanner analyse voltooid."
            )

            self.logger.info(
                (
                    "AI market scan completed | "
                    "requested=%d scanned=%d failed=%d"
                ),
                scan_result.total_requested,
                scan_result.total_scanned,
                scan_result.total_failed,
            )

        except Exception as error:

            self.logger.exception(
                "AI market scan failed: %s",
                error,
            )

            self.window.dashboard_page.set_status_text(
                f"AI Scanner mislukt: {error}"
            )

            self.window.scanner_page.set_status_text(
                f"AI Scanner mislukt: {error}"
            )