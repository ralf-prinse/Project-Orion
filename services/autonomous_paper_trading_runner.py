from __future__ import annotations

import time

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingCycleResult,
    AutonomousPaperTradingResult,
)
from services.stores.repositories.paper_portfolio_repository import (
    PaperPortfolioRepository,
)
from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.live_paper_market_scanner import LivePaperMarketScanner
from services.portfolio_allocator import PortfolioAllocator
from services.trading_cycle import TradingCycle


class AutonomousPaperTradingRunner:
    """
    Finite autonomous paper trading runner.

    Responsibilities
    ----------------
    - Preserve one TradingSession across multiple cycles
    - Run live market scan
    - Allocate portfolio capital
    - Execute approved paper trades
    - Return immutable autonomous result

    Does NOT
    --------
    - Fetch market data directly
    - Rank candidates directly
    - Place real broker orders
    """

    def __init__(
        self,
        config: AutonomousPaperTradingConfig | None = None,
        scanner: LivePaperMarketScanner | None = None,
        allocator: PortfolioAllocator | None = None,
        trading_cycle: TradingCycle | None = None,
        portfolio_repository: PaperPortfolioRepository | None = None,
    ):
        self.config = config or AutonomousPaperTradingConfig()
        self.scanner = scanner or LivePaperMarketScanner(
            config=self.config.live_config,
        )
        self.allocator = allocator or PortfolioAllocator()
        self.trading_cycle = trading_cycle or TradingCycle()
        self.portfolio_repository = portfolio_repository

    def run(self) -> AutonomousPaperTradingResult:
        session = TradingSession(
            name="Orion Autonomous Paper Trading",
            portfolio=self._load_or_create_portfolio(),
        )
        

        cycle_results: list[AutonomousPaperTradingCycleResult] = []
        completed_cycles = 0
        failed_cycles = 0

        for cycle_index in range(self.config.cycles):
            try:
                scan_result = self.scanner.run(
                    session=session,
                )

                allocation_result = self.allocator.allocate(
                    session=session,
                    candidates=scan_result.candidates,
                    config=self.config.live_config,
                )

                executed_trades = 0
                rejected_trades = 0

                for decision in allocation_result.decisions:
                    if not decision.approved:
                        rejected_trades += 1
                        continue

                    cycle_result = self.trading_cycle.run(
                        session=session,
                        snapshot=MarketSnapshot(
                            symbol=decision.symbol,
                            current_price=(
                                decision.candidate.result.risk_plan.entry_price
                            ),
                            pipeline_result=decision.candidate.result,
                        ),
                        quantity=decision.quantity,
                    )

                    session = cycle_result.session

                    if cycle_result.action == "OPEN_POSITION":
                        executed_trades += 1
                    else:
                        rejected_trades += 1

                cycle_results.append(
                    AutonomousPaperTradingCycleResult(
                        scan=scan_result,
                        allocation=allocation_result,
                        executed_trades=executed_trades,
                        rejected_trades=rejected_trades,
                    )
                )

                completed_cycles += 1
                self._save_portfolio(
                    session.portfolio,
                )

                if self.config.print_cycle_summary:
                    self._print_cycle_summary(
                        cycle_index=cycle_index + 1,
                        scanned=scan_result.scanned_symbols,
                        executed=executed_trades,
                        rejected=rejected_trades,
                        session=session,
                    )

            except Exception:
                failed_cycles += 1

                if self.config.stop_on_exception:
                    break

            if (
                self.config.sleep_seconds > 0
                and cycle_index < self.config.cycles - 1
            ):
                time.sleep(self.config.sleep_seconds)

        return AutonomousPaperTradingResult(
            session=session,
            cycle_results=cycle_results,
            completed_cycles=completed_cycles,
            failed_cycles=failed_cycles,
            initial_cash=self.config.live_config.initial_cash,
            final_cash=session.cash,
            final_equity=session.equity,
        )

    def _load_or_create_portfolio(self) -> PaperPortfolio:
        if (
            self.portfolio_repository is not None
            and self.portfolio_repository.exists()
        ):
            return self.portfolio_repository.load()

        return PaperPortfolio(
            cash=self.config.live_config.initial_cash,
        )

    def _save_portfolio(
        self,
        portfolio: PaperPortfolio,
    ) -> None:
        if self.portfolio_repository is None:
            return

        self.portfolio_repository.save(
            portfolio,
        )


    def _print_cycle_summary(
        self,
        cycle_index: int,
        scanned: int,
        executed: int,
        rejected: int,
        session: TradingSession,
    ) -> None:
        print(
            f"Cycle {cycle_index}: "
            f"scanned={scanned}, "
            f"executed={executed}, "
            f"rejected={rejected}, "
            f"cash=€{session.cash:.2f}, "
            f"equity=€{session.equity:.2f}"
        )