from collections.abc import Sequence
from time import perf_counter
from typing import Any

from core.orchestration.scan_context import ScanContext
from core.orchestration.scan_pipeline_step import ScanPipelineStep
from core.orchestration.scan_statistics import ScanStatistics
from core.orchestration.scan_step import ScanStep, ScanStepResult
from core.orchestration.scan_summary import ScanSummary
from core.events import (
    EventBus,
    PipelineFailedEvent,
    PipelineStepCompletedEvent,
    PipelineStepStartedEvent,
    ScanCompletedEvent,
    ScanStartedEvent,
)


class ScanOrchestrator:
    """
    Central end-to-end scan orchestrator for Project Orion.

    The orchestrator coordinates scan execution, progress reporting, timing and
    error handling. It deliberately contains no market-data, analysis, signal,
    decision, risk, portfolio, planner, AI or GUI logic.

    Sprint 10.10 promotes the orchestrator from a single pipeline wrapper to a
    deterministic step-driven integration layer. Existing services can be
    adapted through ScanStep implementations while the public API remains stable
    for GUI, CLI, scheduler and future API usage.
    """

    def __init__(
        self,
        scan_pipeline: Any | None = None,
        scan_steps: Sequence[ScanStep] | None = None,
        clock: Any | None = None,
        event_bus: EventBus | None = None,
    ):
        self.scan_pipeline = scan_pipeline
        self.scan_steps = list(scan_steps) if scan_steps is not None else None
        self.clock = clock or perf_counter
        self.event_bus = event_bus

    def _create_default_scan_pipeline(self) -> Any:
        # Lazy import keeps core.orchestration importable in environments where
        # optional market-data provider dependencies are not installed.
        from services.scanner.scan_pipeline import ScanPipeline

        return ScanPipeline()

    def _resolve_scan_steps(self) -> list[ScanStep]:
        if self.scan_steps is not None:
            return list(self.scan_steps)

        pipeline = self.scan_pipeline or self._create_default_scan_pipeline()
        return [ScanPipelineStep(scan_pipeline=pipeline)]

    def run(
        self,
        scan_context: ScanContext | list[str] | None = None,
    ) -> ScanSummary:
        context = self._resolve_context(scan_context)
        symbols = context.resolved_symbols()

        statistics = ScanStatistics(
            symbols_requested=len(symbols),
        )

        total_start = self.clock()

        context.emit_progress(
            stage="scan",
            message="Scan started.",
            percent=0.0,
            current=0,
            total=len(symbols),
        )
        self._publish_event(ScanStartedEvent(symbols=symbols))

        if not symbols:
            statistics.add_message("Geen symbolen ontvangen.")
            statistics.total_seconds = self._elapsed_since(total_start)
            context.emit_progress(
                stage="scan",
                message="Scan completed without symbols.",
                percent=100.0,
                current=0,
                total=0,
                completed=True,
            )
            summary = ScanSummary(statistics=statistics)
            self._publish_event(ScanCompletedEvent(summary=summary))
            return summary

        try:
            summary = self._run_steps(
                context=context,
                symbols=symbols,
                statistics=statistics,
            )

            statistics.total_seconds = self._elapsed_since(total_start)

            context.emit_progress(
                stage="scan",
                message="Scan completed.",
                percent=100.0,
                current=len(symbols),
                total=len(symbols),
                completed=True,
            )

            self._publish_event(ScanCompletedEvent(summary=summary))
            return summary

        except Exception as exc:
            error_message = f"Scan failed: {exc}"
            statistics.add_error(error_message)
            statistics.symbols_failed = len(symbols)
            statistics.total_seconds = self._elapsed_since(total_start)

            context.emit_progress(
                stage="scan",
                message=error_message,
                percent=100.0,
                current=0,
                total=len(symbols),
                completed=True,
                failed=True,
            )
            self._publish_event(
                PipelineFailedEvent(
                    error_message=error_message,
                    exception_type=exc.__class__.__name__,
                )
            )

            if not context.continue_on_error:
                raise

            summary = ScanSummary(statistics=statistics)
            self._publish_event(ScanCompletedEvent(summary=summary))
            return summary

    def _run_steps(
        self,
        context: ScanContext,
        symbols: list[str],
        statistics: ScanStatistics,
    ) -> ScanSummary:
        steps = self._resolve_scan_steps()
        payload: Any = symbols
        opportunities: list[Any] = []
        pipeline_status: Any | None = None
        stage_results: dict[str, Any] = {}

        if not steps:
            statistics.add_message("Geen scan-stappen geconfigureerd.")
            statistics.symbols_processed = 0
            statistics.symbols_failed = len(symbols)
            return ScanSummary(statistics=statistics)

        total_steps = len(steps)

        for index, step in enumerate(steps, start=1):
            step_name = self._step_name(step)
            start_percent = self._step_progress_percent(index - 1, total_steps)
            end_percent = self._step_progress_percent(index, total_steps)

            context.emit_progress(
                stage=step_name,
                message=f"Starting {step_name}.",
                percent=start_percent,
                current=index - 1,
                total=total_steps,
            )
            self._publish_event(
                PipelineStepStartedEvent(
                    step_name=step_name,
                    index=index,
                    total=total_steps,
                )
            )

            step_start = self.clock()
            step_result = step.run(payload)
            step_seconds = self._elapsed_since(step_start)
            statistics.add_timing(step_name, step_seconds)

            payload = step_result.payload
            stage_results[step_name] = payload

            self._copy_step_result(
                statistics=statistics,
                symbols=symbols,
                step_name=step_name,
                step_result=step_result,
            )

            if step_result.opportunities:
                opportunities = list(step_result.opportunities)

            if step_result.pipeline_status is not None:
                pipeline_status = step_result.pipeline_status
                self._copy_pipeline_stage_timings(
                    statistics=statistics,
                    pipeline_status=pipeline_status,
                )

            context.emit_progress(
                stage=step_name,
                message=f"Completed {step_name}.",
                percent=end_percent,
                current=index,
                total=total_steps,
                completed=index == total_steps,
            )
            self._publish_event(
                PipelineStepCompletedEvent(
                    step_name=step_name,
                    index=index,
                    total=total_steps,
                    duration_seconds=step_seconds,
                )
            )

        if statistics.symbols_processed == 0 and statistics.symbols_failed == 0:
            statistics.symbols_processed = len(symbols)

        return ScanSummary(
            opportunities=opportunities,
            pipeline_status=pipeline_status,
            statistics=statistics,
            stage_results=stage_results,
        )

    def _copy_step_result(
        self,
        statistics: ScanStatistics,
        symbols: list[str],
        step_name: str,
        step_result: ScanStepResult,
    ) -> None:
        if step_result.symbols_processed is not None:
            statistics.symbols_processed = int(step_result.symbols_processed)

        if step_result.symbols_failed is not None:
            statistics.symbols_failed = int(step_result.symbols_failed)

        if step_result.opportunities_count is not None:
            statistics.opportunities_count = int(step_result.opportunities_count)
        elif step_result.opportunities:
            statistics.opportunities_count = len(step_result.opportunities)

        for message in step_result.messages:
            statistics.add_message(message)

        statistics.add_message(f"Scan step completed: {step_name}")

        if step_result.symbols_processed is None and step_result.symbols_failed is None:
            statistics.symbols_processed = len(symbols)

    def _copy_pipeline_stage_timings(
        self,
        statistics: ScanStatistics,
        pipeline_status: Any,
    ) -> None:
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="quotes",
            attribute="quote_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="price_filter",
            attribute="price_filter_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="volume_filter",
            attribute="volume_filter_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="liquidity_filter",
            attribute="liquidity_filter_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="relative_strength_filter",
            attribute="relative_strength_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="momentum_filter",
            attribute="momentum_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="technical_scanner",
            attribute="technical_scanner_seconds",
        )
        self._copy_stage_timing(
            statistics=statistics,
            pipeline_status=pipeline_status,
            stage="ranking",
            attribute="ranking_seconds",
        )

    def _copy_stage_timing(
        self,
        statistics: ScanStatistics,
        pipeline_status: Any,
        stage: str,
        attribute: str,
    ) -> None:
        duration = getattr(pipeline_status, attribute, None)

        if duration is None:
            return

        statistics.add_timing(stage, float(duration))

    def _resolve_context(
        self,
        scan_context: ScanContext | list[str] | None,
    ) -> ScanContext:
        if scan_context is None:
            return ScanContext()

        if isinstance(scan_context, ScanContext):
            return scan_context

        return ScanContext(symbols=list(scan_context))

    def _step_name(self, step: ScanStep) -> str:
        name = getattr(step, "name", None)

        if name:
            return str(name)

        return step.__class__.__name__

    def _step_progress_percent(self, completed_steps: int, total_steps: int) -> float:
        if total_steps <= 0:
            return 100.0

        return round((completed_steps / total_steps) * 100.0, 2)

    def _publish_event(self, event: Any) -> None:
        if self.event_bus is None:
            return

        self.event_bus.publish(event)

    def _elapsed_since(self, start: float) -> float:
        return round(float(self.clock() - start), 6)
