from __future__ import annotations

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
from services.live_paper_market_scanner import (
    LivePaperMarketScanner,
)
from services.paper_position_update_service import (
    PaperPositionUpdateService,
)
from services.portfolio_allocator import PortfolioAllocator
from services.portfolio_revaluation_service import (
    PortfolioRevaluationService,
)
from services.position_monitor import PositionMonitor
from services.position_exit_execution_service import (
    PositionExitExecutionService,
)
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
from services.market_session_service import MarketSessionService


class AutonomousPaperTradingRunner:
    def __init__(
        self,
        config=None,
        scanner=None,
        allocator=None,
        trading_cycle=None,
        portfolio_repository=None,
        trading_session_repository=None,
        trade_journal_repository=None,
        decision_journal_repository=None,
        trade_journal_builder=None,
        position_update_service=None,
        position_monitor=None,
        revaluation_service=None,
        price_provider=None,
        exit_engine=None,
        position_exit_execution_service=None,
        trading_session_sync_service=None,
        market_session_service: MarketSessionService | None = None,
    ):
        self.config = config or AutonomousPaperTradingConfig()
        self.scanner = scanner or LivePaperMarketScanner(
            config=self.config.live_config,
        )
        self.allocator = allocator or PortfolioAllocator()
        self.trading_cycle = trading_cycle or TradingCycle()
        self.portfolio_repository = portfolio_repository
        self.trading_session_repository = (
            trading_session_repository
        )
        self.trade_journal_repository = (
            trade_journal_repository
        )
        self.decision_journal_repository = (
            decision_journal_repository
        )
        self.trade_journal_builder = (
            trade_journal_builder
            or TradeJournalBuilder()
        )
        self.position_update_service = (
            position_update_service
            or PaperPositionUpdateService()
        )
        self.position_monitor = (
            position_monitor
            or PositionMonitor()
        )
        self.revaluation_service = (
            revaluation_service
            or PortfolioRevaluationService()
        )
        self.price_provider = price_provider or YahooProvider()
        self.exit_engine = exit_engine or ExitEngine()

        self.position_exit_execution_service = (
            position_exit_execution_service
        )

        self.trading_session_sync_service = (
            trading_session_sync_service
        )
        self.market_session_service = market_session_service

    def run(self):
        session_id = self._build_session_id()
        session = self._load_or_create_session()
        peak_portfolio_value = max(
            session.peak_portfolio_value,
            session.equity,
        )
        session.peak_portfolio_value = peak_portfolio_value
        cycle_results = []
        completed_cycles = 0
        failed_cycles = 0

        for cycle_index in range(self.config.cycles):
            cycle_number = cycle_index + 1

            try:
                if self.trading_session_sync_service is not None:
                    session = (
                        self.trading_session_sync_service
                        .synchronize(session)
                    )

                session = self._update_open_position_lifecycle(
                    session
                )
                session = self._process_open_position_exits(
                    session,
                    cycle_number,
                    session_id,
                )
                peak_portfolio_value = max(
                    peak_portfolio_value,
                    session.equity,
                )
                session.peak_portfolio_value = (
                    peak_portfolio_value
                )

                scan_result = self.scanner.run(
                    session=session
                )
                allocation_result = self.allocator.allocate(
                    session=session,
                    candidates=scan_result.candidates,
                    config=self.config.live_config,
                )

                executed_trades = 0
                rejected_trades = 0
                attempted_trade = False
                opened_symbols: set[str] = set()

                for decision in allocation_result.decisions:
                    if not decision.approved:
                        rejected_trades += 1
                        continue

                    attempted_trade = True

                    cycle_result = self.trading_cycle.run(
                        session=session,
                        snapshot=MarketSnapshot(
                            symbol=decision.symbol,
                            current_price=(
                                decision
                                .candidate
                                .result
                                .risk_plan
                                .entry_price
                            ),
                            pipeline_result=(
                                decision.candidate.result
                            ),
                        ),
                        quantity=decision.quantity,
                    )

                    session = cycle_result.session

                    if cycle_result.action == "OPEN_POSITION":
                        executed_trades += 1
                        opened_symbols.add(
                            decision.symbol.strip().upper()
                        )
                        self._append_open_trade_journal_entry(
                            decision=decision,
                            session=session,
                            cycle_number=cycle_number,
                            session_id=session_id,
                        )
                    else:
                        rejected_trades += 1

                if (
                    attempted_trade
                    and self.trading_session_sync_service is not None
                ):
                    if opened_symbols:
                        session = (
                            self.trading_session_sync_service
                            .synchronize(
                                session,
                                expected_symbols=opened_symbols,
                                attempts=8,
                                retry_delay_seconds=0.25,
                            )
                        )
                    else:
                        session = (
                            self.trading_session_sync_service
                            .synchronize(session)
                        )

                peak_portfolio_value = max(
                    peak_portfolio_value,
                    session.equity,
                )
                session.peak_portfolio_value = (
                    peak_portfolio_value
                )

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

            except Exception as exc:
                failed_cycles += 1
                print(
                    "Autonomous cycle failed: "
                    f"{repr(exc)}"
                )

                if self.config.stop_on_exception:
                    break

        result = AutonomousPaperTradingResult(
            session=session,
            cycle_results=cycle_results,
            completed_cycles=completed_cycles,
            failed_cycles=failed_cycles,
            initial_cash=self.config.live_config.initial_cash,
            final_cash=session.cash,
            final_equity=session.equity,
        )

        self._save_decision_journal(
            result=result,
            session_id=session_id,
        )

        return result

    def _update_open_position_lifecycle(
        self,
        session,
    ):
        updated_session = session
        fallback_prices = {}

        for symbol in list(session.portfolio.positions):
            try:
                current_price = (
                    self.price_provider
                    .get_current_price(symbol)
                )
            except Exception as exc:
                print(
                    f"Position update skipped for {symbol}: "
                    f"{repr(exc)}"
                )
                continue

            has_state = (
                symbol
                in updated_session.position_states
            )
            has_risk_plan = (
                symbol
                in updated_session.risk_plans
            )

            if has_state and has_risk_plan:
                update_result = (
                    self.position_update_service
                    .update_position(
                        session=updated_session,
                        symbol=symbol,
                        current_price=current_price,
                    )
                )

                if update_result.updated:
                    updated_session = update_result.session
                    continue

            fallback_prices[symbol] = current_price

        if fallback_prices:
            fallback_portfolio = (
                self.revaluation_service.revalue(
                    portfolio=updated_session.portfolio,
                    prices=fallback_prices,
                )
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

        return updated_session

    def _process_open_position_exits(
        self,
        session,
        cycle_number,
        session_id,
    ):
        """
        Evaluate and execute exits for all currently open positions.

        Preferred execution path:

        PositionMonitor
        -> PositionExitExecutionService
        -> ExecutionEngine
        -> Broker
        -> Broker Truth Synchronization
        -> TradingSession
        -> Journal

        When no PositionExitExecutionService is configured, the legacy
        local ExitEngine remains available for backwards compatibility
        with existing paper-trading tests and runtimes.
        """

        updated_session = session

        for original_position in list(
            session.portfolio.positions.values()
        ):
            symbol = (
                original_position.symbol
                .strip()
                .upper()
            )

            # A previous exit in this same cycle may already have caused
            # broker truth synchronization to remove this position.
            position = (
                updated_session
                .portfolio
                .positions
                .get(symbol)
            )

            if position is None:
                continue

            state = updated_session.position_states.get(
                symbol
            )
            risk_plan = updated_session.risk_plans.get(
                symbol
            )

            if (
                state is not None
                and risk_plan is not None
            ):
                decision = (
                    self.position_monitor
                    .evaluate_managed(
                        position=position,
                        state=state,
                        risk_plan=risk_plan,
                        config=self.config.live_config,
                    )
                )
            else:
                decision = (
                    self.position_monitor.evaluate(
                        position,
                        self.config.live_config,
                    )
                )

            if decision.action == "HOLD":
                continue

            if (
                self.market_session_service is not None
                and not self.market_session_service.is_symbol_market_open(
                    symbol
                )
            ):
                print(
                    "Position exit skipped for "
                    f"{symbol}: regular market session is closed."
                )
                continue

            if (
                self.position_exit_execution_service is not None
                and (
                    state is None
                    or risk_plan is None
                )
            ):
                print(
                    "Broker position exit skipped for "
                    f"{symbol}: position is not managed by Orion "
                    "(PositionState or RiskPlan is missing)."
                )
                continue

            if (
                self.position_exit_execution_service
                is not None
            ):
                updated_session = (
                    self._execute_broker_position_exit(
                        session=updated_session,
                        position=position,
                        decision=decision,
                        cycle_number=cycle_number,
                        session_id=session_id,
                    )
                )
                continue

            updated_session = (
                self._execute_legacy_local_exit(
                    session=updated_session,
                    position=position,
                    decision=decision,
                    cycle_number=cycle_number,
                    session_id=session_id,
                )
            )

        return updated_session
        

    def _execute_broker_position_exit(
        self,
        *,
        session,
        position,
        decision,
        cycle_number,
        session_id,
    ):
        """
        Execute one managed exit through ExecutionEngine and replace
        provisional local state with authoritative broker truth.
        """

        exit_result = (
            self.position_exit_execution_service
            .execute(
                session=session,
                decision=decision,
            )
        )

        if not exit_result.attempted:
            return session

        engine_result = exit_result.execution_result

        if engine_result is None:
            return session

        execution = engine_result.execution

        if not execution.accepted:
            print(
                "Position exit rejected for "
                f"{position.symbol}: "
                f"{execution.status} - "
                f"{execution.message}"
            )
            return session

        executed_quantity = execution.executed_quantity

        if executed_quantity <= 0:
            print(
                "Position exit returned no executed "
                f"quantity for {position.symbol}."
            )
            return session

        expected_remaining_quantity = (
            position.quantity
            - executed_quantity
        )

        if expected_remaining_quantity < 0:
            raise RuntimeError(
                "Executed SELL quantity exceeds the "
                "open position quantity for "
                f"{position.symbol}."
            )

        provisional_session = TradingSession(
            name=session.name,
            portfolio=engine_result.portfolio,
            position_states=dict(
                session.position_states
            ),
            risk_plans=dict(
                session.risk_plans
            ),
            status=session.status,
        )

        if self.trading_session_sync_service is not None:
            synchronized_session = (
                self.trading_session_sync_service
                .synchronize(
                    provisional_session,
                    expected_position_quantities={
                        position.symbol:
                        expected_remaining_quantity,
                    },
                    attempts=8,
                    retry_delay_seconds=0.25,
                )
            )
        else:
            synchronized_session = provisional_session

            if expected_remaining_quantity == 0:
                synchronized_session.position_states.pop(
                    position.symbol,
                    None,
                )
                synchronized_session.risk_plans.pop(
                    position.symbol,
                    None,
                )

        self._append_broker_exit_journal_entry(
            position=position,
            decision=decision,
            execution=execution,
            cycle_number=cycle_number,
            session_id=session_id,
        )

        return synchronized_session

    def _execute_legacy_local_exit(
        self,
        *,
        session,
        position,
        decision,
        cycle_number,
        session_id,
    ):
        """
        Preserve the historical local PaperBroker exit route when no
        broker-neutral exit execution service has been configured.

        This path exists for backwards compatibility only.
        """

        portfolio = session.portfolio
        position_states = dict(
            session.position_states
        )
        risk_plans = dict(
            session.risk_plans
        )

        result = self.exit_engine.execute(
            portfolio=portfolio,
            decision=decision,
        )

        if not result.executed:
            return session

        self._append_exit_journal_entry(
            position,
            result.action,
            decision.reason,
            cycle_number,
            session_id,
        )

        closed_symbol = (
            result.symbol
            .strip()
            .upper()
        )

        position_states.pop(
            closed_symbol,
            None,
        )
        risk_plans.pop(
            closed_symbol,
            None,
        )

        return TradingSession(
            name=session.name,
            portfolio=portfolio,
            position_states=position_states,
            risk_plans=risk_plans,
            status=session.status,
        )

    def _append_open_trade_journal_entry(
        self,
        decision,
        session,
        cycle_number,
        session_id,
    ):
        if self.trade_journal_repository is None:
            return

        position = session.portfolio.positions.get(
            decision.symbol
        )

        if position is None:
            return

        entry = (
            self.trade_journal_builder
            .build_open_trade_entry(
                decision=decision,
                position=position,
                cycle_number=cycle_number,
                session_id=session_id,
            )
        )

        self.trade_journal_repository.append(
            entry
        )

    def _append_broker_exit_journal_entry(
        self,
        *,
        position,
        decision,
        execution,
        cycle_number,
        session_id,
    ):
        """
        Journal a confirmed broker SELL using actual fill information.

        This method is called only after successful broker execution and
        successful broker-truth synchronization.
        """

        if self.trade_journal_repository is None:
            return

        executed_quantity = (
            execution.executed_quantity
        )
        executed_price = execution.executed_price

        invested_amount = round(
            position.entry_price
            * executed_quantity,
            2,
        )

        exit_value = round(
            executed_price
            * executed_quantity,
            2,
        )

        entry = TradeJournalEntry(
            timestamp=(
                execution.executed_at
                or datetime.now()
            ),
            symbol=position.symbol,
            action="CLOSE_POSITION",
            decision=decision.action,
            confidence=1.0,
            score=0.0,
            entry_price=position.entry_price,
            exit_price=executed_price,
            quantity=executed_quantity,
            invested_amount=invested_amount,
            realized_profit_loss=round(
                exit_value - invested_amount,
                2,
            ),
            unrealized_profit_loss=0.0,
            expected_risk=0.0,
            regime="UNKNOWN",
            volatility="UNKNOWN",
            ai_summary=(
                "Exit executed through broker-neutral "
                "position lifecycle: "
                f"{decision.action}"
            ),
            recommendation_reason=decision.reason,
            cycle_number=cycle_number,
            session_id=session_id,
        )

        self.trade_journal_repository.append(
            entry
        )

    def _append_exit_journal_entry(
        self,
        position,
        action,
        reason,
        cycle_number,
        session_id,
    ):
        if self.trade_journal_repository is None:
            return

        invested_amount = position.cost_basis
        exit_value = position.market_value

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
            realized_profit_loss=round(
                exit_value - invested_amount,
                2,
            ),
            unrealized_profit_loss=0.0,
            expected_risk=0.0,
            regime="UNKNOWN",
            volatility="UNKNOWN",
            ai_summary=(
                "Exit executed by position "
                f"management runtime: {action}"
            ),
            recommendation_reason=reason,
            cycle_number=cycle_number,
            session_id=session_id,
        )

        self.trade_journal_repository.append(
            entry
        )

    def _load_or_create_session(self):
        if (
            self.trading_session_repository is not None
            and self.trading_session_repository.exists()
        ):
            return (
                self.trading_session_repository.load()
            )

        return TradingSession(
            name="Orion Autonomous Paper Trading",
            portfolio=self._load_or_create_portfolio(),
        )

    def _load_or_create_portfolio(self):
        if (
            self.portfolio_repository is not None
            and self.portfolio_repository.exists()
        ):
            return self.portfolio_repository.load()

        return PaperPortfolio(
            cash=self.config.live_config.initial_cash
        )

    def _save_session(self, session):
        if self.trading_session_repository is not None:
            self.trading_session_repository.save(
                session
            )

        if self.portfolio_repository is not None:
            self.portfolio_repository.save(
                session.portfolio
            )

    def _save_decision_journal(
        self,
        result,
        session_id,
    ):
        if self.decision_journal_repository is None:
            return

        entries = (
            self.trade_journal_builder
            .build_decision_entries(
                result=result,
                session_id=session_id,
            )
        )

        for entry in entries:
            self.decision_journal_repository.append(
                entry
            )

    def _build_session_id(self):
        return (
            "autonomous-"
            + datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
        )
