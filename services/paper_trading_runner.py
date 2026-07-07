from __future__ import annotations

from models.market_snapshot import MarketSnapshot
from models.paper_trading_run_result import PaperTradingRunResult
from models.trading_session import TradingSession
from services.trading_cycle import TradingCycle


class PaperTradingRunner:
    """
    Runs multiple deterministic TradingCycle ticks.

    No market data fetching.
    No AI.
    No real broker.
    """

    def __init__(
        self,
        trading_cycle: TradingCycle | None = None,
    ):
        self.trading_cycle = trading_cycle or TradingCycle()

    def run(
        self,
        session: TradingSession,
        snapshots: list[MarketSnapshot],
        quantity: int = 1,
    ) -> PaperTradingRunResult:

        current_session = session
        cycles = []

        for snapshot in snapshots:
            cycle_result = self.trading_cycle.run(
                session=current_session,
                snapshot=snapshot,
                quantity=quantity,
            )

            cycles.append(cycle_result)
            current_session = cycle_result.session

        return PaperTradingRunResult(
            session=current_session,
            cycles=cycles,
        )