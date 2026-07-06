from __future__ import annotations

from dataclasses import replace

from models.trade_lifecycle import Trade
from services.analysis.models import AnalysisResult
from services.exit_evaluation_service import ExitEvaluationService
from services.trade_lifecycle_service import TradeLifecycleService


class TradeMonitorService:
    """
    Monitors all open trades.

    Responsibilities
    ----------------
    - Iterate over every open trade
    - Refresh trade prices
    - Keep trade statistics up-to-date
    - Delegate lifecycle updates
    - Delegate exit evaluation

    Does NOT:
    - Make BUY decisions
    - Persist trades directly
    """

    def __init__(
        self,
        trade_lifecycle_service: TradeLifecycleService,
        exit_evaluation_service: ExitEvaluationService | None = None,
    ) -> None:
        self._trade_lifecycle = trade_lifecycle_service
        self._exit_evaluation_service = (
            exit_evaluation_service or ExitEvaluationService()
        )

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
        trades = self.get_open_trades()

        return len(trades)