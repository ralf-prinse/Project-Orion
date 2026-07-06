from __future__ import annotations

from dataclasses import replace

from models.trade_lifecycle import Trade
from providers.yahoo_provider import YahooProvider
from services.analysis.models import AnalysisResult
from services.exit_evaluation_service import ExitEvaluationService
from services.trade_lifecycle_service import TradeLifecycleService


class TradeMonitorService:
    """
    Monitors all open trades.

    Responsibilities
    ----------------
    - Iterate over every open trade
    - Refresh current market prices
    - Keep trade statistics up-to-date
    - Delegate lifecycle updates
    - Delegate exit evaluation

    Does NOT:
    - Make BUY decisions
    - Persist trades directly
    - Render UI
    """

    def __init__(
        self,
        trade_lifecycle_service: TradeLifecycleService,
        exit_evaluation_service: ExitEvaluationService | None = None,
        market_provider: YahooProvider | None = None,
    ) -> None:
        self._trade_lifecycle = trade_lifecycle_service
        self._exit_evaluation_service = (
            exit_evaluation_service or ExitEvaluationService()
        )
        self._market_provider = market_provider or YahooProvider()

    def get_open_trades(self) -> list[Trade]:
        return self._trade_lifecycle.get_open_trades()

    def update_trade(
        self,
        symbol: str,
        current_price: float,
    ) -> None:
        self._trade_lifecycle.update_trade_price(
            symbol=symbol,
            current_price=current_price,
        )

    def evaluate_trade(
        self,
        trade: Trade,
        analysis: AnalysisResult | None = None,
    ) -> Trade:
        (
            exit_signal,
            exit_score,
            summary,
            exit_reasons,
            trend_status,
            momentum_status,
            risk_status,
        ) = self._exit_evaluation_service.evaluate(
            trade=trade,
            analysis=analysis,
        )

        return replace(
            trade,
            exit_signal=exit_signal,
            exit_reason=summary,
        )

    def evaluate_all(
        self,
        analysis_by_symbol: dict[str, AnalysisResult] | None = None,
    ) -> list[Trade]:
        analysis_by_symbol = analysis_by_symbol or {}

        evaluated: list[Trade] = []

        for trade in self.get_open_trades():
            evaluated.append(
                self.evaluate_trade(
                    trade=trade,
                    analysis=analysis_by_symbol.get(trade.symbol.upper()),
                )
            )

        return evaluated

    def refresh_all(self) -> int:
        """
        Refresh all open trades with current market prices.

        This method performs the deterministic backend refresh only.
        It does not render UI and does not close trades automatically.
        """

        refreshed_count = 0

        for trade in self.get_open_trades():
            current_price = self._market_provider.get_current_price(
                trade.symbol
            )

            self.update_trade(
                symbol=trade.symbol,
                current_price=current_price,
            )

            refreshed_count += 1

        return refreshed_count

    def refresh_and_evaluate_all(
        self,
        analysis_by_symbol: dict[str, AnalysisResult] | None = None,
    ) -> list[Trade]:
        """
        Refresh prices and return evaluated open trades.

        Exit advice is updated in the returned Trade objects.
        OpenTradeStore is updated with refreshed price/P/L data.
        """

        self.refresh_all()

        return self.evaluate_all(
            analysis_by_symbol=analysis_by_symbol,
        )