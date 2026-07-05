from services.analysis.models import AnalysisResult
from models.position_monitor import PositionMonitorResult
from models.trade_lifecycle import Trade
from services.exit_evaluation_service import ExitEvaluationService


class PositionMonitorService:
    """
    Deterministic service for monitoring an open trade.

    Responsibilities:
    - calculate portfolio metrics
    - delegate exit decisions to ExitEvaluationService
    - build PositionMonitorResult

    No AI.
    No UI.
    """

    def __init__(
        self,
        exit_evaluation_service: ExitEvaluationService | None = None,
    ):
        self.exit_evaluation_service = (
            exit_evaluation_service or ExitEvaluationService()
        )

    def evaluate(
        self,
        trade: Trade,
        analysis: AnalysisResult | None = None,
    ) -> PositionMonitorResult:
        invested_amount = round(
            trade.quantity * trade.entry_price,
            2,
        )

        market_value = round(
            trade.quantity * trade.current_price,
            2,
        )

        unrealized_profit_loss = round(
            market_value - invested_amount,
            2,
        )

        if invested_amount > 0:
            unrealized_profit_loss_percent = round(
                (unrealized_profit_loss / invested_amount) * 100,
                2,
            )
        else:
            unrealized_profit_loss_percent = 0.0

        (
            exit_signal,
            exit_score,
            summary,
            exit_reasons,
            trend_status,
            momentum_status,
            risk_status,
        ) = self.exit_evaluation_service.evaluate(
            trade=trade,
            analysis=analysis,
        )

        stop_loss_distance = round(
            trade.current_price - trade.stop_loss,
            2,
        )

        take_profit_distance = round(
            trade.take_profit - trade.current_price,
            2,
        )

        return PositionMonitorResult(
            trade=trade,
            exit_signal=exit_signal,
            exit_score=exit_score,
            reason=summary,
            exit_reasons=exit_reasons,
            trend_status=trend_status,
            momentum_status=momentum_status,
            risk_status=risk_status,
            market_value=market_value,
            invested_amount=invested_amount,
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_profit_loss_percent=unrealized_profit_loss_percent,
            stop_loss_distance=stop_loss_distance,
            take_profit_distance=take_profit_distance,
        )