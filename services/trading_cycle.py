from __future__ import annotations

from models.market_snapshot import MarketSnapshot
from models.trading_cycle_result import TradingCycleResult
from models.trading_session import TradingSession
from services.paper_position_close_service import PaperPositionCloseService
from services.paper_position_update_service import PaperPositionUpdateService
from services.paper_trading_service import PaperTradingService


class TradingCycle:
    def __init__(
        self,
        paper_trading_service: PaperTradingService | None = None,
        update_service: PaperPositionUpdateService | None = None,
        close_service: PaperPositionCloseService | None = None,
    ):
        self.paper_trading_service = (
            paper_trading_service or PaperTradingService()
        )
        self.update_service = (
            update_service or PaperPositionUpdateService()
        )
        self.close_service = (
            close_service or PaperPositionCloseService()
        )

    def run(
        self,
        session: TradingSession,
        snapshot: MarketSnapshot,
        quantity: int = 1,
    ) -> TradingCycleResult:
        symbol = snapshot.symbol.upper()

        if symbol in session.portfolio.positions:
            update_result = self.update_service.update_position(
                session=session,
                symbol=symbol,
                current_price=snapshot.current_price,
            )

            if not update_result.updated:
                return TradingCycleResult(
                    symbol=symbol,
                    session=session,
                    action="UPDATE_FAILED",
                    message=update_result.message,
                    updated=update_result,
                )

            updated_state = update_result.position_state

            if (
                updated_state is not None
                and snapshot.current_price
                <= updated_state.current_stop_loss
            ):
                close_result = self.close_service.close_position(
                    session=update_result.session,
                    symbol=symbol,
                    exit_price=snapshot.current_price,
                )

                return TradingCycleResult(
                    symbol=symbol,
                    session=close_result.session,
                    action="CLOSE_POSITION",
                    message=close_result.message,
                    updated=update_result,
                    closed=close_result,
                )

            return TradingCycleResult(
                symbol=symbol,
                session=update_result.session,
                action="UPDATE_POSITION",
                message=update_result.message,
                updated=update_result,
            )

        pipeline_input = snapshot.resolved_pipeline_output

        if pipeline_input is None:
            return TradingCycleResult(
                symbol=symbol,
                session=session,
                action="NO_ACTION",
                message="No open position and no pipeline result.",
            )

        open_result = self.paper_trading_service.open_position(
            session=session,
            pipeline_output=pipeline_input,
            quantity=quantity,
        )

        return TradingCycleResult(
            symbol=symbol,
            session=open_result.session,
            action=(
                "OPEN_POSITION"
                if open_result.executed
                else "OPEN_REJECTED"
            ),
            message=open_result.message,
            opened=open_result,
        )
