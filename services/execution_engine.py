from __future__ import annotations

from dataclasses import dataclass

from models.execution_context import ExecutionContext
from models.execution_result import ExecutionResult
from models.paper_portfolio import PaperPortfolio
from models.portfolio_snapshot import PortfolioSnapshot
from services.execution_report_builder import (
    ExecutionReport,
    ExecutionReportBuilder,
)
from services.execution_validator import (
    ExecutionValidationResult,
    ExecutionValidator,
)
from services.order_factory import OrderFactory
from services.paper_broker import PaperBroker
from services.portfolio_manager import PortfolioManager


@dataclass(frozen=True)
class ExecutionEngineResult:
    """
    Complete deterministic result of one execution cycle.
    """

    validation: ExecutionValidationResult
    execution: ExecutionResult
    portfolio: PaperPortfolio
    snapshot: PortfolioSnapshot
    report: ExecutionReport


class ExecutionEngine:
    """
    Central execution orchestrator.

    Responsibilities
    ----------------
    - Validate execution context
    - Create broker-neutral order
    - Execute through broker adapter
    - Apply execution to portfolio
    - Build portfolio snapshot
    - Build execution report

    Does NOT
    --------
    - Generate BUY / HOLD / SELL
    - Generate RiskPlan
    - Modify TradingPipeline decisions
    - Use AI
    """

    def __init__(
        self,
        validator: ExecutionValidator | None = None,
        order_factory: OrderFactory | None = None,
        broker: PaperBroker | None = None,
        portfolio_manager: PortfolioManager | None = None,
        report_builder: ExecutionReportBuilder | None = None,
    ):
        self.validator = validator or ExecutionValidator()
        self.order_factory = order_factory or OrderFactory()
        self.broker = broker or PaperBroker()
        self.portfolio_manager = portfolio_manager or PortfolioManager()
        self.report_builder = report_builder or ExecutionReportBuilder()

    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionEngineResult:

        validation = self.validator.validate(context)

        if not validation.is_valid:
            execution = ExecutionResult(
                accepted=False,
                status="REJECTED",
                order=None,
                message="Execution validation failed: "
                + " ".join(validation.errors),
            )

            snapshot = self.portfolio_manager.snapshot(
                context.portfolio,
            )

            report = self.report_builder.build(
                context=context,
                result=execution,
                snapshot=snapshot,
            )

            return ExecutionEngineResult(
                validation=validation,
                execution=execution,
                portfolio=context.portfolio,
                snapshot=snapshot,
                report=report,
            )

        order = self.order_factory.create(context)

        execution = self.broker.execute(order)

        updated_portfolio = self.portfolio_manager.apply_execution(
            portfolio=context.portfolio,
            result=execution,
        )

        snapshot = self.portfolio_manager.snapshot(
            updated_portfolio,
        )

        report = self.report_builder.build(
            context=context,
            result=execution,
            snapshot=snapshot,
        )

        return ExecutionEngineResult(
            validation=validation,
            execution=execution,
            portfolio=updated_portfolio,
            snapshot=snapshot,
            report=report,
        )