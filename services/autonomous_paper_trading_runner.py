from __future__ import annotations

import time
from datetime import datetime

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingCycleResult,
    AutonomousPaperTradingResult,
)
from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trade_journal_entry import TradeJournalEntry
from models.trading_session import TradingSession
from providers.yahoo_provider import YahooProvider
from services.exit_engine import ExitEngine
from services.live_paper_market_scanner import LivePaperMarketScanner
from services.paper_position_update_service import (
    PaperPositionUpdateService,
)
from services.portfolio_allocator import PortfolioAllocator
from services.portfolio_revaluation_service import (
    PortfolioRevaluationService,
)
from services.position_monitor import PositionMonitor
from services.stores.repositories.paper_portfolio_repository import (
    PaperPortfolioRepository,
)
from services.stores.repositories.trade_journal_repository import (
    TradeJournalRepository,
)
from services.stores.repositories.trading_session_repository import (
    TradingSessionRepository,
)
from services.trade_journal_builder import TradeJournalBuilder
from services.trading_cycle import TradingCycle


class AutonomousPaperTradingRunner:
    """
    Finite autonomous paper trading runner.

    Responsibilities:
    - load or create a complete TradingSession
    - update existing position lifecycle state
    - evaluate and execute exits
    - scan for new candidates
    - allocate capital
    - execute paper trades
    - persist complete session state
    - append trade-journal entries

    Does NOT:
    - generate trading decisions directly
    - calculate indicators
    - calculate risk plans directly
    - use AI for trading decisions
    """

    def __init__(
        self,
        config: AutonomousPaperTradingConfig | None = None,
        scanner: LivePaperMarketScanner | None = None,
        allocator: PortfolioAllocator | None = None,
        trading_cycle: TradingCycle | None = None,
        portfolio_repository: PaperPortfolioRepository | None = None,
        trading_session_repository: TradingSessionRepository | None = None,
        trade_journal_repository: TradeJournalRepository | None = None,
        trade_journal_builder: TradeJournalBuilder | None = None,
        position_update_service: PaperPositionUpdateService | None = None,
        position_monitor: PositionMonitor | None = None,
        revaluation_service: PortfolioRevaluationService | None = None,
        price_provider: YahooProvider | None = None,
        exit_engine: ExitEngine | None = None,
    ):
        self.config = config or AutonomousPaperTradingConfig()

        self.scanner = scanner or LivePaperMarketScanner(
            config=self.config.live_config,
        )

        self.allocator = allocator or PortfolioAllocator()
        self.trading_cycle = trading_cycle or TradingCycle()

        self.portfolio_repository = portfolio_repository
        self.trading_session_repository = trading_session_repository

        self.trade_journal_repository = trade_journal_repository
        self.trade_journal_builder = (
            trade_journal_builder or TradeJournalBuilder()
        )

        self.position_update_service = (
            position_update_service or PaperPositionUpdateService()
        )

        self.position_monitor = position_monitor or PositionMonitor()

        self.revaluation_service = (
            revaluation_service or PortfolioRevaluationService()
        )

        self.price_provider = price_provider or YahooProvider()
        self.exit_engine = exit_engine or ExitEngine()

    def run(self) -> AutonomousPaperTradingResult:
        session_id = self._build_session_id()
        session = self._load_or_create_session()

        cycle_results: list[AutonomousPaperTradingCycleResult] = []
        completed_cycles = 0
        failed_cycles = 0

        for cycle_index in range(self.config.cycles):
            try:
                session = self._update_open_position_lifecycle(
                    session=session,
                )

                session = self._process_open_position_exits(
                    session=session,
                    cycle_number=cycle_index + 1,
                    session_id=session_id,
                )

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

                self._save_session(session)

                if self.config.print_cycle_summary:
                    self._print_cycle_summary(
                        cycle_index=cycle_index + 1,
                        scanned=scan_result.scanned_symbols,
                        executed=executed_trades,
                        rejected=rejected_trades,
                        session=session,
                    )

            except Exception as exc:
                failed_cycles += 1

                print(
                    "Autonomous cycle failed: "
                    f"{repr(exc)}"
                )

                if self.config.stop_on_exception:
                    break

            if (
                self.config.sleep_seconds > 0
                and cycle_index < self.config.cycles - 1
            ):
                time.sleep(self.config.sleep_seconds)

        result = AutonomousPaperTradingResult(
            session=session,
            cycle_results=cycle_results,
            completed_cycles=completed_cycles,
            failed_cycles=failed_cycles,
            initial_cash=self.config.live_config.initial_cash,
            final_cash=session.cash,
            final_equity=session.equity,
        )

        self._save_trade_journal(
            result=result,
            session_id=session_id,
        )

        return result

    def _update_open_position_lifecycle(
        self,
        session: TradingSession,
    ) -> TradingSession:
        """
        Update all open positions with current market prices.

        Positions with a persisted PositionState and RiskPlan use the
        complete deterministic position-management lifecycle.

        Legacy positions without lifecycle state use portfolio
        revaluation only, preserving backward compatibility.
        """

        updated_session = session
        fallback_prices: dict[str, float] = {}
        updated_positions = 0

        for symbol in list(session.portfolio.positions):
            try:
                current_price = self.price_provider.get_current_price(
                    symbol
                )
            except Exception as exc:
                print(
                    f"Position update skipped for {symbol}: "
                    f"{repr(exc)}"
                )
                continue

            has_state = symbol in updated_session.position_states
            has_risk_plan = symbol in updated_session.risk_plans

            if has_state and has_risk_plan:
                update_result = (
                    self.position_update_service.update_position(
                        session=updated_session,
                        symbol=symbol,
                        current_price=current_price,
                    )
                )

                if update_result.updated:
                    updated_session = update_result.session
                    updated_positions += 1

                    management = update_result.position_update

                    if management is not None:
                        actions = management.management.actions

                        if actions:
                            print(
                                f"Position lifecycle: {symbol} | "
                                + ", ".join(actions)
                            )

                    continue

                print(
                    f"Lifecycle update failed for {symbol}: "
                    f"{update_result.message}"
                )

            fallback_prices[symbol] = current_price

        if fallback_prices:
            fallback_portfolio = self.revaluation_service.revalue(
                portfolio=updated_session.portfolio,
                prices=fallback_prices,
            )

            updated_session = TradingSession(
                name=updated_session.name,
                portfolio=fallback_portfolio,
                position_states=dict(
                    updated_session.position_states
                ),
                risk_plans=dict(
                    updated_session.risk_plans
                ),
                status=updated_session.status,
            )

        total_updated = updated_positions + len(fallback_prices)

        if total_updated:
            print(
                "Portfolio lifecycle updated: "
                f"{total_updated} position price(s) processed."
            )

        return updated_session

    def _process_open_position_exits(
        self,
        session: TradingSession,
        cycle_number: int,
        session_id: str,
    ) -> TradingSession:
        portfolio = session.portfolio
        position_states = dict(session.position_states)
        risk_plans = dict(session.risk_plans)

        for position in list(portfolio.positions.values()):
            decision = self.position_monitor.evaluate(
                position=position,
                config=self.config.live_config,
            )

            print(
                f"Position monitor: "
                f"{decision.symbol} -> {decision.action} "
                f"({decision.unrealized_return_percent * 100:.2f}%) "
                f"{decision.reason}"
            )

            result = self.exit_engine.execute(
                portfolio=portfolio,
                decision=decision,
            )

            if not result.executed:
                continue

            print(
                f"Exit executed: "
                f"{result.symbol} -> {result.action} | "
                f"{result.reason}"
            )

            self._append_exit_journal_entry(
                position=position,
                action=result.action,
                reason=result.reason,
                cycle_number=cycle_number,
                session_id=session_id,
            )

            symbol = result.symbol.upper()

            position_states.pop(symbol, None)
            risk_plans.pop(symbol, None)

        return TradingSession(
            name=session.name,
            portfolio=portfolio,
            position_states=position_states,
            risk_plans=risk_plans,
            status=session.status,
        )

    def _append_exit_journal_entry(
        self,
        position,
        action: str,
        reason: str,
        cycle_number: int,
        session_id: str,
    ) -> None:
        if self.trade_journal_repository is None:
            return

        invested_amount = position.cost_basis
        exit_value = position.market_value

        realized_profit_loss = round(
            exit_value - invested_amount,
            2,
        )

        entry = TradeJournalEntry(
            timestamp=datetime.now(),
            symbol=position.symbol,
            action="CLOSE_POSITION",
            decision=action,
            confidence=1.0,
            score=0.0,
            entry_price=position.entry_price,
            exit_price=position.current_price,
            quantity=position.quantity,
            invested_amount=invested_amount,
            realized_profit_loss=realized_profit_loss,
            unrealized_profit_loss=0.0,
            expected_risk=0.0,
            regime="UNKNOWN",
            volatility="UNKNOWN",
            ai_summary=(
                f"Exit executed by PositionMonitor: {action}"
            ),
            recommendation_reason=reason,
            cycle_number=cycle_number,
            session_id=session_id,
        )

        self.trade_journal_repository.append(entry)

    def _load_or_create_session(self) -> TradingSession:
        if (
            self.trading_session_repository is not None
            and self.trading_session_repository.exists()
        ):
            return self.trading_session_repository.load()

        return TradingSession(
            name="Orion Autonomous Paper Trading",
            portfolio=self._load_or_create_portfolio(),
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

    def _save_session(
        self,
        session: TradingSession,
    ) -> None:
        if self.trading_session_repository is not None:
            self.trading_session_repository.save(session)

        if self.portfolio_repository is not None:
            self.portfolio_repository.save(
                session.portfolio
            )

    def _save_trade_journal(
        self,
        result: AutonomousPaperTradingResult,
        session_id: str,
    ) -> None:
        if self.trade_journal_repository is None:
            return

        entries = self.trade_journal_builder.build(
            result=result,
            session_id=session_id,
        )

        for entry in entries:
            self.trade_journal_repository.append(entry)

    def _build_session_id(self) -> str:
        return (
            "autonomous-"
            + datetime.now().strftime("%Y%m%d-%H%M%S")
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