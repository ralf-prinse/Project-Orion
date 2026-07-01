from time import perf_counter
from typing import Any

from core.orchestration.scan_context import ScanContext
from core.orchestration.scan_statistics import ScanStatistics
from core.orchestration.scan_summary import ScanSummary
class ScanOrchestrator:
    """
    Central end-to-end scan orchestrator for Project Orion.

    The orchestrator coordinates scan execution, progress reporting, timing and
    error handling. It deliberately contains no market-data, analysis, signal,
    decision, risk, portfolio or GUI logic.

    Sprint 10.9 introduces this as a stable foundation around the existing
    ScanPipeline. Later sprints can enrich this orchestrator with additional
    deterministic layers while preserving this public API.
    """

    def __init__(
        self,
        scan_pipeline: Any | None = None,
        clock: Any | None = None,
    ):
        self.scan_pipeline = scan_pipeline or self._create_default_scan_pipeline()
        self.clock = clock or perf_counter

    def _create_default_scan_pipeline(self) -> Any:
        # Lazy import keeps core.orchestration importable in environments where
        # optional market-data provider dependencies are not installed.
        from services.scanner.scan_pipeline import ScanPipeline

        return ScanPipeline()

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
            return ScanSummary(statistics=statistics)

        try:
            pipeline_start = self.clock()
            pipeline_result = self.scan_pipeline.run(symbols)
            pipeline_seconds = self._elapsed_since(pipeline_start)
            statistics.add_timing("scan_pipeline", pipeline_seconds)

            opportunities = list(getattr(pipeline_result, "opportunities", []))
            pipeline_status = getattr(pipeline_result, "status", None)

            self._copy_pipeline_statistics(
                statistics=statistics,
                symbols=symbols,
                opportunities=opportunities,
                pipeline_status=pipeline_status,
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

            return ScanSummary(
                opportunities=opportunities,
                pipeline_status=pipeline_status,
                statistics=statistics,
            )

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

            if not context.continue_on_error:
                raise

            return ScanSummary(statistics=statistics)

    def _resolve_context(
        self,
        scan_context: ScanContext | list[str] | None,
    ) -> ScanContext:
        if scan_context is None:
            return ScanContext()

        if isinstance(scan_context, ScanContext):
            return scan_context

        return ScanContext(symbols=list(scan_context))

    def _copy_pipeline_statistics(
        self,
        statistics: ScanStatistics,
        symbols: list[str],
        opportunities: list[Any],
        pipeline_status: Any | None,
    ) -> None:
        statistics.symbols_processed = len(symbols)
        statistics.opportunities_count = len(opportunities)

        if pipeline_status is None:
            return

        technical_results_count = getattr(
            pipeline_status,
            "technical_results_count",
            None,
        )
        if technical_results_count is not None:
            statistics.symbols_processed = int(technical_results_count)
            statistics.symbols_failed = max(
                0,
                len(symbols) - statistics.symbols_processed,
            )

        opportunities_count = getattr(pipeline_status, "opportunities_count", None)
        if opportunities_count is not None:
            statistics.opportunities_count = int(opportunities_count)

        for message in getattr(pipeline_status, "messages", []) or []:
            statistics.add_message(message)

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

    def _elapsed_since(self, start: float) -> float:
        return round(float(self.clock() - start), 6)
